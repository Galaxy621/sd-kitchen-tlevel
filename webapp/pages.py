import os
from flask import Blueprint, render_template, session, url_for

# Blueprint is a way to organize a group of related views and other code.
bp = Blueprint('pages', __name__)

@bp.context_processor
def handle_context():
    return dict(os = os)

@bp.route("/")
def index():
    return render_template("index.html.j2", title="Recipes")