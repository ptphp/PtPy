# -*- coding: utf-8 -*-
import logging
import os
import tempfile
import sys
import time
import logging
import subprocess

from PySide.QtNetwork   import QNetworkCookieJar
from PySide.QtNetwork   import QNetworkAccessManager
from PySide.QtNetwork   import QNetworkRequest
from PySide.QtNetwork   import QNetworkDiskCache
from PySide.QtNetwork   import QNetworkProxy

from PySide.QtCore      import qInstallMsgHandler
from PySide.QtCore      import QByteArray
from PySide.QtCore      import QUrl
from PySide.QtCore      import QSize
from PySide.QtCore      import Qt

from PySide.QtCore      import QtDebugMsg
from PySide.QtCore      import QtWarningMsg
from PySide.QtCore      import QtCriticalMsg
from PySide.QtCore      import QtFatalMsg

from PySide.QtGui       import QApplication

from PySide.QtWebKit    import QWebPage
from PySide.QtWebKit    import QWebSettings

from PySide import QtWebKit

PYSIDE = True

logger = logging.getLogger('ptwebkit')
default_user_agent = "ptwebkit"

class Logger(logging.Logger):
    @staticmethod
    def log(message, sender="PtWebkit", level="info"):
        if not hasattr(logger, level):
            raise Error('invalid log level')
        getattr(logger, level)("%s: %s", sender, message)

class Error(Exception):
    """Base class for Ghost exceptions."""
    pass


class TimeoutError(Error):
    """Raised when a request times out"""
    pass
class QTMessageProxy(object):
    def __init__(self, debug=False):
        self.debug = debug

    def __call__(self, msgType, msg):
        if msgType == QtDebugMsg and self.debug:
            Logger.log(msg, sender='QT', level='debug')
        elif msgType == QtWarningMsg and self.debug:
            Logger.log(msg, sender='QT', level='warning')
        elif msgType == QtCriticalMsg:
            Logger.log(msg, sender='QT', level='critical')
        elif msgType == QtFatalMsg:
            Logger.log(msg, sender='QT', level='fatal')
        elif self.debug:
            Logger.log(msg, sender='QT', level='info')

class PtWebPage(QWebPage):
    """Overrides QtWebKit.QWebPage in order to intercept some graphical
    behaviours like alert(), confirm().
    Also intercepts client side console.log().
    """
    def __init__(self, app, ptwebkit):
        self.ptwebkit = ptwebkit
        super(PtWebPage, self).__init__(app)

    def chooseFile(self, frame, suggested_file=None):
        return PtWebkit._upload_file

    def javaScriptConsoleMessage(self, message, line, source):
        """Prints client console message in current output stream."""
        super(PtWebPage, self).javaScriptConsoleMessage(message, line,
            source)
        log_type = "error" if "Error" in message else "info"
        Logger.log("%s(%d): %s" % (source or '<unknown>', line, message),
        sender="Frame", level=log_type)

    def javaScriptAlert(self, frame, message):
        """Notifies ptwebkit for alert, then pass."""
        PtWebkit._alert = message
        self.ptwebkit.append_popup_message(message)
        Logger.log("alert('%s')" % message, sender="Frame")

    def javaScriptConfirm(self, frame, message):
        """Checks if ptwebkit is waiting for confirm, then returns the right
        value.
        """
        if PtWebkit._confirm_expected is None:
            raise Error('You must specified a value to confirm "%s"' %
                message)
        self.ptwebkit.append_popup_message(message)
        confirmation, callback = PtWebkit._confirm_expected
        Logger.log("confirm('%s')" % message, sender="Frame")
        if callback is not None:
            return callback()
        return confirmation

    def javaScriptPrompt(self, frame, message, defaultValue, result=None):
        """Checks if ptwebkit is waiting for prompt, then enters the right
        value.
        """
        if PtWebkit._prompt_expected is None:
            raise Error('You must specified a value for prompt "%s"' %
                message)
        self.ptwebkit.append_popup_message(message)
        result_value, callback = PtWebkit._prompt_expected
        Logger.log("prompt('%s')" % message, sender="Frame")
        if callback is not None:
            result_value = callback()
        if result_value == '':
            Logger.log("'%s' prompt filled with empty string" % message,
                level='warning')

        if result is None:
            # PySide
            return True, result_value
        result.append(unicode(result_value))
        return True

    def setUserAgent(self, user_agent):
        self.user_agent = user_agent

    def userAgentForUrl(self, url):
        return self.user_agent

class HttpResource(object):
    """Represents an HTTP resource.
    """
    def __init__(self, reply, cache, content=None):
        self.url = reply.url().toString()
        self.content = content
        if cache and self.content is None:
            # Tries to get back content from cache
            if PYSIDE:
                buffer = cache.data(reply.url().toString())
            else:
                buffer = cache.data(reply.url())
            if buffer is not None:
                content = buffer.readAll()
        try:
            self.content = unicode(content)
        except UnicodeDecodeError:
            self.content = content
        self.http_status = reply.attribute(
            QNetworkRequest.HttpStatusCodeAttribute)
        Logger.log("Resource loaded: %s %s" % (self.url, self.http_status))
        self.headers = {}
        for header in reply.rawHeaderList():
            try:
                self.headers[unicode(header)] = unicode(
                    reply.rawHeader(header))
            except UnicodeDecodeError:
                # it will lose the header value,
                # but at least not crash the whole process
                logger.error(
                    "Invalid characters in header {0}={1}"
                    % (header, reply.rawHeader(header))
                )
        self._reply = reply

class PtWebkit:
    _alert  = None
    _app    = None
    def __init__(self,
            user_agent=default_user_agent,
            wait_timeout=8,
            wait_callback=None,
            log_level=logging.WARNING,
            display=False,
            viewport_size=(800, 600),
            ignore_ssl_errors=True,
            cache_dir=os.path.join(tempfile.gettempdir(), "ptwebkit.py"),
            plugins_enabled=False,
            java_enabled=False,
            plugin_path=['/usr/lib/mozilla/plugins', ],
            download_images=True,
            qt_debug=False,
            show_scroolbars=True,
            network_access_manager_class=None):
        
        self.http_resources = []
        self.user_agent = user_agent
        self.wait_callback = wait_callback
        self.wait_timeout = wait_timeout

        self.display = display

        if sys.platform.startswith('linux') and not 'DISPLAY' in os.environ\
                and not hasattr(PtWebkit, 'xvfb'):
            try:
                os.environ['DISPLAY'] = ':99'
                PtWebkit.xvfb = subprocess.Popen(['Xvfb', ':99'])
            except OSError:
                raise Error('Xvfb is required to a ghost run outside ' +
                            'an X instance')

        if not PtWebkit._app:
            PtWebkit._app = QApplication.instance() or QApplication(['ghost'])
            qInstallMsgHandler(QTMessageProxy(qt_debug))
            if plugin_path:
                for p in plugin_path:
                    PtWebkit._app.addLibraryPath(p)

        if network_access_manager_class is not None:
            self.page.setNetworkAccessManager(network_access_manager_class())

        self.page = PtWebPage(PtWebkit._app, self)
        QWebSettings.setMaximumPagesInCache(0)
        QWebSettings.setObjectCacheCapacities(0, 0, 0)
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.LocalStorageEnabled, True)

        self.page.setForwardUnsupportedContent(True)
        self.page.settings().setAttribute(
            QWebSettings.AutoLoadImages, download_images)
        self.page.settings().setAttribute(
            QWebSettings.PluginsEnabled, plugins_enabled)
        self.page.settings().setAttribute(QWebSettings.JavaEnabled,
            java_enabled)

        if not show_scroolbars:
            self.page.mainFrame().setScrollBarPolicy(Qt.Vertical,
                Qt.ScrollBarAlwaysOff)
            self.page.mainFrame().setScrollBarPolicy(Qt.Horizontal,
                Qt.ScrollBarAlwaysOff)

        self.set_viewport_size(*viewport_size)


        # Page signals
        self.page.loadFinished.connect(self._page_loaded)
        self.page.loadStarted.connect(self._page_load_started)
        self.page.unsupportedContent.connect(self._unsupported_content)

        self.manager = self.page.networkAccessManager()
        
        self.manager.finished.connect(self._request_ended)
        self.manager.sslErrors.connect(self._on_manager_ssl_errors)
        # Cache
        if cache_dir:
            self.cache = QNetworkDiskCache()
            self.cache.setCacheDirectory(cache_dir)
            self.manager.setCache(self.cache)
        else:
            self.cache = None

        
        # Cookie jar
        self.cookie_jar = QNetworkCookieJar()
        self.manager.setCookieJar(self.cookie_jar)

        self.main_frame = self.page.mainFrame()

        # User Agent
        self.page.setUserAgent(self.user_agent)
        
        #logger.setLevel(log_level)

        class GhostQWebView(QtWebKit.QWebView):
            def sizeHint(self):
                return QSize(*viewport_size)

        self.webview = GhostQWebView()

        if plugins_enabled:
            self.webview.settings().setAttribute(
                QtWebKit.QWebSettings.PluginsEnabled, True)
        if java_enabled:
            self.webview.settings().setAttribute(
                QtWebKit.QWebSettings.JavaEnabled, True)

        self.webview.setPage(self.page)

        if self.display:
            self.webview.show()
            
    def show(self):
        """Show current page inside a QWebView.
        """
        self.webview.show()
        
    def hide(self):
        """Close the webview."""
        try:
            self.webview.close()
        except:
            raise Error("no webview to close")
        
    def set_proxy(self, type_, host='localhost', port=8888, user='',
            password=''):
        """Set up proxy for FURTHER connections.

        :param type_: proxy type to use: \
            none/default/socks5/https/http.
        :param host: proxy server ip or host name.
        :param port: proxy port.
        """
        _types = {
            'default': QNetworkProxy.DefaultProxy,
            'none': QNetworkProxy.NoProxy,
            'socks5': QNetworkProxy.Socks5Proxy,
            'https': QNetworkProxy.HttpProxy,
            'http': QNetworkProxy.HttpCachingProxy
        }

        if type_ is None:
            type_ = 'none'
        type_ = type_.lower()
        if type_ in ['none', 'default']:
            self.manager.setProxy(QNetworkProxy(_types[type_]))
            return
        elif type_ in _types:
            proxy = QNetworkProxy(_types[type_], hostName=host, port=port,
                user=user, password=password)
            self.manager.setProxy(proxy)
        else:
            raise ValueError('Unsupported proxy type:' + type_ \
            + '\nsupported types are: none/socks5/http/https/default')
        
        self.manager.finished.connect(self._request_ended)
        self.manager.sslErrors.connect(self._on_manager_ssl_errors)
        
    def set_viewport_size(self, width, height):
        """Sets the page viewport size.

        :param width: An integer that sets width pixel count.
        :param height: An integer that sets height pixel count.
        """
        self.page.setViewportSize(QSize(width, height))
    def delete_cookies(self):
        """Deletes all cookies."""
        self.cookie_jar.setAllCookies([])

    def clear_alert_message(self):
        """Clears the alert message"""
        self._alert = None


    def open(self, address, method='get', headers={}, auth=None, body=None,
             default_popup_response=None, wait=True):
        """Opens a web page.

        :param address: The resource URL.
        :param method: The Http method.
        :param headers: An optional dict of extra request hearders.
        :param auth: An optional tuple of HTTP auth (username, password).
        :param body: An optional string containing a payload.
        :param default_popup_response: the default response for any confirm/
        alert/prompt popup from the Javascript (replaces the need for the with
        blocks)
        :param wait: If set to True (which is the default), this
        method call waits for the page load to complete before
        returning.  Otherwise, it just starts the page load task and
        it is the caller's responsibilty to wait for the load to
        finish by other means (e.g. by calling wait_for_page_loaded()).
        :return: Page resource, and all loaded resources, unless wait
        is False, in which case it returns None.
        """
        body = body or QByteArray()
        try:
            method = getattr(QNetworkAccessManager,
                             "%sOperation" % method.capitalize())
        except AttributeError:
            raise Error("Invalid http method %s" % method)
        request = QNetworkRequest(QUrl(address))
        request.CacheLoadControl(0)
        for header in headers:
            request.setRawHeader(header, headers[header])
        self._auth = auth
        self._auth_attempt = 0  # Avoids reccursion

        self.main_frame.load(request, method, body)
        self.loaded = False

        if default_popup_response is not None:
            PtWebkit._prompt_expected = (default_popup_response, None)
            PtWebkit._confirm_expected = (default_popup_response, None)

        if wait:
            return self.wait_for_page_loaded()
    @property
    def content(self, to_unicode=True):
        """Returns current frame HTML as a string.

        :param to_unicode: Whether to convert html to unicode or not
        """
        if to_unicode:
            return unicode(self.main_frame.toHtml())
        else:
            return self.main_frame.toHtml()

    def wait_for_page_loaded(self):
        """Waits until page is loaded, assumed that a page as been requested.
        """
        self.wait_for(lambda: self.loaded,
                      'Unable to load requested page')
        resources = self._release_last_resources()
        page = None

        url = self.main_frame.url().toString()
        url_without_hash = url.split("#")[0]

        for resource in resources:
            if url == resource.url or url_without_hash == resource.url:
                page = resource
        return page, resources

    def wait_for(self, condition, timeout_message):
        """Waits until condition is True.

        :param condition: A callable that returns the condition.
        :param timeout_message: The exception message on timeout.
        """
        started_at = time.time()
        while not condition():
            if time.time() > (started_at + self.wait_timeout):
                raise TimeoutError(timeout_message)
            time.sleep(0.01)
            PtWebkit._app.processEvents()
            if self.wait_callback is not None:
                self.wait_callback()

    def _page_loaded(self):
        """Called back when page is loaded.
        """
        self.loaded = True
        if self.cache:
            self.cache.clear()


    def _page_load_started(self):
        """Called back when page load started.
        """
        self.loaded = False
    def _release_last_resources(self):
        """Releases last loaded resources.

        :return: The released resources.
        """
        last_resources = self.http_resources
        self.http_resources = []
        return last_resources
    def _request_ended(self, reply):
        """Adds an HttpResource object to http_resources.

        :param reply: The QNetworkReply object.
        """

        if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute):
            Logger.log("[%s] bytesAvailable()= %s" % (str(reply.url()),
                reply.bytesAvailable()), level="debug")

            # Some web pages return cache headers that mandates not to cache
            # the reply, which means we won't find this QNetworkReply in
            # the cache object. In this case bytesAvailable will return > 0.
            # Such pages are www.etsy.com
            # This is a bit of a hack and due to the async nature of QT, might
            # not work at times. We should move to using some proxied
            # implementation of QNetworkManager and QNetworkReply in order to
            # get the contents of the requests properly rather than relying
            # on the cache.
            if reply.bytesAvailable() > 0:
                content = reply.peek(reply.bytesAvailable())
            else:
                content = None
            self.http_resources.append(HttpResource(reply, self.cache,
                                                    content=content))
    def _unsupported_content(self, reply):
        reply.readyRead.connect(
            lambda reply=reply: self._reply_download_content(reply))


    def _reply_download_content(self, reply):
        """Adds an HttpResource object to http_resources with unsupported
        content.

        :param reply: The QNetworkReply object.
        """
        if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute):
            self.http_resources.append(HttpResource(reply, self.cache,
                                                    reply.readAll()))
    def _on_manager_ssl_errors(self, reply, errors):
        url = unicode(reply.url().toString())
        if self.ignore_ssl_errors:
            reply.ignoreSslErrors()
        else:
            Logger.log('SSL certificate error: %s' % url, level='warning')