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
    if meal_name: return recipes.search_by_name(meal_name).as_dict()
    
    meal_id = request.args.get("id")
    if meal_id: return recipes.get_by_id(meal_id).as_dict()

    return make_response("<h1>400 Bad Request</h1>You must provide a valid argument (name, id)", 400)

@bp.route("/")
def index():
    return render_template("index.html.j2", title="Recipes")

@bp.route("/about")
def about():
    return render_template("about.html.j2", title="About")