import os
from lib import uimodules

settings = dict(
                template_path   = os.path.join(os.path.dirname(__file__), 'template'),
                static_path     = os.path.join(os.path.dirname(__file__), 'static/'),
                upload_path     = os.path.join(os.path.dirname(__file__), 'static/upload'),
                cookie_secret   = "SZUzonpBQIuXE3yKBtWPre2N5AS7jEQKv0Kioj9iKT0=",
                login_url       = '/signin',
                xsrf_cookies    = True,
                ui_modules      = uimodules,
                autoescape      = None,
                memcache_host   = 'localhost:11211',
                debug           = False
                )