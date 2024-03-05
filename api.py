import json
import requests

from dataclasses import dataclass, asdict
from flask import make_response

meal_cache = {}

@dataclass
class Ingredient:
    name: str
    measurement: str

@dataclass
class Meal():
    id: int
    name: str
    area: str
    category: str
    tags: list[str]

    instructions: list[str]
    ingredients: list[Ingredient]

    drink_alternative: str
    thumbnail: str
    youtube: str

    as_dict = asdict
    
    def __post_init__(self):
        meal_cache[self.id] = self

    @classmethod
    def create_from_dict(cls, meal: dict):
        ingredients = []

        for i in range(20): # Read each ingredient and turn into an object
            ingredient = meal.get(f"strIngredient{i + 1}", "").strip()
            measurement = meal.get(f"strMeasure{i + 1}", "").strip()
            if ingredient == "": break # There are no more ingredients, stop.
            ingredients.append(Ingredient(ingredient, measurement))

        inst1 = meal["strInstructions"].split(". ")
        instructions = []

        for string in inst1:
            results = string.split("\n")
            for r in results: instructions.append(r.strip())

        obj = cls(
            int(meal["idMeal"]),
            meal["strMeal"],
            meal["strArea"],
            meal["strCategory"],
            meal["strTags"],

            instructions,
            ingredients,

            meal.get("strDrinkAlternative", None),
            meal.get("strMealThumb", None),
            meal.get("strYoutube", None)
        )

        # obj.json = meal
        return obj


class RecipeWrapper:
    # Singleton Creation
    # Ensures that only one instance of the class exists
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecipeWrapper, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, url: str = "https://www.themealdb.com/api/json/v1/", api_key: str = "1"):
        self.API_key = api_key
        self.change_url(url)

    def change_url(self, url: str) -> None:
        self.URL = url + self.API_key + "/"

    def change_api_key(self, api: str) -> None:
        self.API_key = api
        self.URL = self.URL + self.API_key + "/"

    def search(self, query: str) -> dict | None:
        request = requests.get(self.URL + "search.php" + query)
        if request.status_code != 200: return None
        return request.json()
    
    def lookup(self, query: str) -> dict | None:
        request = requests.get(self.URL + "lookup.php" + query)
        if request.status_code != 200: return None
        return request.json()
    
    def from_result(self, result, force_new: bool = False):
        if not result: return None

        meals = result["meals"]
        if meals is None: return None
        if len(meals) <= 0: return None

        meal = meals[0]
        cached = meal_cache.get(int(meal["idMeal"]), None) if not force_new else None
        obj = cached or Meal.create_from_dict(meals[0])
        
        return obj

    def search_by_name(self, name: str, force_new: bool = False):
        result = self.search("?s=" + name)
        return self.from_result(result)
    
    def get_by_id(self, id: int):
        result = self.lookup(f"?i={id}")
        return self.from_result(result)
