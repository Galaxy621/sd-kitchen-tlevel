import json
import requests

from flask import make_response

class RecipeWrapper:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecipeWrapper, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, url: str = "https://www.themealdb.com/api/json/v1/1/"):
        self.change_url(url)

    def change_url(self, url: str) -> None:
        self.URL = url

    def search(self, query: str) -> dict | None:
        request = requests.get(self.URL + "search.php" + query)
        if request.status_code != 200: return None
        return request.json()
    
    def search_by_name(self, name: str):
        result = self.search("?s=" + name)
        if not result: return None
        
        meals = result["meals"]
        if meals is None: return None
        if len(meals) <= 0: return None
        return meals[0]