import os
from flask import Blueprint, render_template, make_response, request

from api import RecipeWrapper

# Blueprint is a way to organize a group of related views and other code.
bp = Blueprint('pages', __name__)
recipes = RecipeWrapper()

# @bp.context_processor
# def handle_context():
#     return dict(os = os)

@bp.route("/search")
def search():
    meal_name = request.args.get("name")
    if not meal_name: return make_response("<h1>400 Bad Request</h1>You must provide 'name'", 400)
    return f"{recipes.search_by_name(meal_name)}"

@bp.route("/")
def index():
    return render_template("index.html.j2", title="Recipes")