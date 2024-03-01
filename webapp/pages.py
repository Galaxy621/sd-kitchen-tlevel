from flask import Blueprint, render_template, session, url_for

# Blueprint is a way to organize a group of related views and other code.
bp = Blueprint('pages', __name__)

@bp.route("/")
def index():
    return render_template("index.html.j2")