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
DBNAME = 'pantry'

# TABLES
RECIPE_TABLE = 'recipe'
INGREDIENT_TABLE = 'ingredient'
NUTRITION_TABLE = 'nutrition'
STEP_TABLE = 'step'
DIET_TABLE = 'diet'
STAT_TABLE = 'stat'

# URLS
FOOD_NETWORK_URL = 'https://www.foodnetwork.com/recipes/recipes-a-z'

#WIKIBOOKS
WIKIBOOKS_BASE_URL_TEMPLATE = 'https://en.wikibooks.org'
WIKIBOOKSURL_1 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes'
WIKIBOOKSURL_2 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Baked+Tilapia+with+White+Wine%0ABaked+Tilapia+with+White+Wine#mw-pages'
WIKIBOOKSURL_3 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Bolognese+Sauce+%27Bambi%27%0ABolognese+Sauce+%27Bambi%27#mw-pages'
WIKIBOOKSURL_4 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Chapati%0AChapati#mw-pages'
WIKIBOOKSURL_5 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Christmas+Pudding+I%0AChristmas+Pudding+I#mw-pages'
WIKIBOOKSURL_6 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Dan+Sululu+%28Nigerian+Cassava+Dumplings%29%0ADan+Sululu+%28Nigerian+Cassava+Dumplings%29#mw-pages'
WIKIBOOKSURL_7 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Feij%C3%A3o+Tropeiro+%28Brazilian+Beans+and+Sausage%29%0AFeij%C3%A3o+Tropeiro+%28Brazilian+Beans+and+Sausage%29#mw-pages'
WIKIBOOKSURL_8 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Ginger+Snap%0AGinger+Snap#mw-pages'
WIKIBOOKSURL_9 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Honey+Lime+Pork+Loin%0AHoney+Lime+Pork+Loin#mw-pages'
WIKIBOOKSURL_10 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Khara+Pongal+%28Rice+and+Lentil+Porridge%29%0AKhara+Pongal+%28Rice+and+Lentil+Porridge%29#mw-pages'
WIKIBOOKSURL_11 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Mango+Atchar%0AMango+Atchar#mw-pages'
WIKIBOOKSURL_12 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Musakhan+%28Palestinian+Spiced+Chicken%29%0AMusakhan+%28Palestinian+Spiced+Chicken%29#mw-pages'
WIKIBOOKSURL_13 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Nigerian+Yam+Balls+%28Ji+Akpurakpu%29%0ANigerian+Yam+Balls+%28Ji+Akpurakpu%29#mw-pages'
WIKIBOOKSURL_14 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Peach+Cobbler%0APeach+Cobbler#mw-pages'
WIKIBOOKSURL_15 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Pudina+Hilsa+%28Bengali+Fish+with+Mint%29%0APudina+Hilsa+%28Bengali+Fish+with+Mint%29#mw-pages'
WIKIBOOKSURL_16 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Russian-style+Waffle+Cake%0ARussian-style+Waffle+Cake#mw-pages'
WIKIBOOKSURL_17 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Smoky+Tuna+Melts%0ASmoky+Tuna+Melts#mw-pages'
WIKIBOOKSURL_18 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Stuffed+Courgette%0AStuffed+Courgette#mw-pages'
WIKIBOOKSURL_19 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Tom+Kha+Kai%0ATom+Kha+Kai#mw-pages'
WIKIBOOKSURL_20 = 'https://en.wikibooks.org/w/index.php?title=Category:Recipes&pagefrom=Wonton+Soup%0AWonton+Soup#mw-pages'

# SQL

insertTotalRecipesSQL = """INSERT INTO total_recipes (total) VALUES (%s)"""

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