import os

from flask import Flask, url_for
from . import pages

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    app.register_blueprint(pages.bp)

    return app