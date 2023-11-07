import boto3
import requests
import pymysql
import json
import diets as DietInfo
from recipe import Recipe
from bs4 import BeautifulSoup
from ingredient_parser import parse_ingredient

# Daily Value Constants
DV_CARBS = 275
DV_FAT = 78
DV_PROTEIN = 50
DV_SODIUM = 2300
DV_SUGAR = 50
DV_FIBER = 28
DV_SATURATED_FAT = 20
DV_CHOLESTEROL = 300

dynamodb = boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = 'AKIAUQ5RSVGJSYOLOFNE',
              aws_secret_access_key = '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')

recipe_table = dynamodb.Table('recipe')

count = dynamodb.describe_table(TableName='recipe')
recipe_total_count = count(['Table']['ItemCount'])

# Parses Ingredient String into separate readable parts
def parse_ingredient_string(ingredient_string) -> dict:
    parsed_ingredient = parse_ingredient(ingredient_string)
    quantity = parsed_ingredient["quantity"]
    unit_type = parsed_ingredient["unit"]
    if quantity == 1:
        if unit_type.endswith("s"):
            return {
                'sentence': parsed_ingredient["sentence"],
                'name': parsed_ingredient["name"],
                'quantity': parsed_ingredient["quantity"],
                'unit': parsed_ingredient["unit"][:-1],
                'comment': parsed_ingredient["comment"],
                'other': parsed_ingredient["other"]
            }
    return parsed_ingredient

# Add item to Recipe Table
def put_item(id: int, recipe: Recipe):
    recipe_table.put_item(
        Item={
            "recipe_id": id,
            "name": recipe.title,
            "source": recipe.source,
            "image": recipe.image,
            "url": recipe.url,
            "servings": recipe.servings,
            "site_name": recipe.site_name,
            "total_time": recipe.total_time,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "diets": recipe.diets,
            "calories": recipe.calories,
            "carbs": recipe.carbs,
            "carbs_dv": recipe.dv_carbs,
            "total_fat": recipe.total_fat,
            "total_fat_dv": recipe.dv_total_fat,
            "saturated_fat": recipe.saturated_fat,
            "saturated_fat_dv": recipe.dv_saturated_fat,
            "fiber": recipe.fiber,
            "fiber_dv": recipe.dv_fiber,
            "sugar": recipe.sugar,
            "sugar_dv": recipe.dv_sugar,
            "protein": recipe.protein,
            "protein_dv": recipe.dv_protein,
            "fiber_dv": recipe.dv_fiber,
            "cholesterol": recipe.cholesterol,
            "cholesterol_dv": recipe.dv_cholesterol,
            "sodium": recipe.sodium,
            "sodium_dv": recipe.dv_sodium,
        }
    )

# response = table.put_item(
#     Item={
#         "recipe_id": 1,
#         "name": "Ham"
#     },
# )
# print(response)

