# DAILY VALUE
DV_CALORIES = 2000
DV_CARBS = 275
DV_FAT = 78
DV_PROTEIN = 50
DV_SODIUM = 2300
DV_SUGAR = 50
DV_FIBER = 28
DV_SATURATED_FAT = 20
DV_CHOLESTEROL = 300

# DB INFO
AWS_ACCESS_KEY = 'AKIAUQ5RSVGJSYOLOFNE'
AWS_SECRET_KEY = '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'
REGION_NAME = 'us-east-2'
ENDPOINT = 'pantry-rds-cluster-instance-1.cafbhjmtde7x.us-east-2.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
PASSWORD = 'i#QT>RiY#MC1a8rYcu-yUVNi)k1a'
DBNAME = 'pantry'#'pantry-rds-cluster-instance-1'

# TABLES
RECIPE_TABLE = 'recipe'
INGREDIENT_TABLE = 'ingredient'
NUTRITION_TABLE = 'nutrition'
STEP_TABLE = 'step'
DIET_TABLE = 'diet'
STAT_TABLE = 'stat'

# URLS
FOOD_NETWORK_URL = 'https://www.foodnetwork.com/recipes/recipes-a-z'

# SQL

insertRecipeSQL = """INSERT INTO recipe (title, source, site_name, url, servings, image, total_time, prep_time,
cook_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

insertNutritionInfoSQL = """INSERT INTO nutrition (recipe_id, calories, total_fat, total_fat_dv, saturated_fat, 
saturated_fat_dv, carbohydrates, carbohydrates_dv, fiber, fiber_dv, sugar, sugar_dv, protein, protein_dv, cholesterol, cholesterol_dv,
 sodium, sodium_dv)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    """

insertIngredientSQL = """INSERT INTO ingredient (recipe_id, sentence, name, quantity, unit, comment, other) 
VALUES (%s, %s, %s, %s, %s, %s, %s)"""

insertStepSQL = """INSERT INTO step (recipe_id, text)
         VALUES (%s, %s) 
    """

insertDietSQL = """INSERT INTO diet (recipe_id, type)
         VALUES (%s, %s) 
    """