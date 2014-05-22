import os

from flask import Flask, render_template, url_for, redirect, jsonify
from flask import request, abort, Response, flash
from flask import make_response

from werkzeug import Headers  # @UnresolvedImport

app = Flask(__name__)
app.config['CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'asecret'


@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
	app.run()