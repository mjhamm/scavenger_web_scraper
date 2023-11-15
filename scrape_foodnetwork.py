import boto3
import requests
import pymysql
import json
from constants import *
import diets as DietInfo
from recipe import Recipe
from recipe_stat import RecipeStat
from bs4 import BeautifulSoup
from decimal import Decimal
from utils import *
from ingredient_parser import parse_ingredient

client = boto3.client('rds', region_name = REGION_NAME, aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

connection = pymysql.connect(
    host=ENDPOINT,
    user=USER,
    password=PASSWORD,
    database=DBNAME
)

cursor = connection.cursor()

cursor.execute("select count(*) from recipe")
#idCount: int = cursor.fetchone()[0]

idCount = 0

# -- FUNCTIONS -- #

# Parses Ingredient String into separate readable parts
def parse_ingredient_string(ingredient_string) -> dict:
    parsed_ingredient = parse_ingredient(ingredient_string)
    print(parsed_ingredient)

    if len(parsed_ingredient.amount) != 0:

        quantity = parsed_ingredient.amount[0].quantity
        if (quantity.__contains__('.')):
            if (quantity.startswith('0')):
                quantity = dec_to_proper_frac(Decimal(checkStringContainsDecimal(quantity))).split('0')[1].strip()
            else:
                quantity = dec_to_proper_frac(Decimal(checkStringContainsDecimal(quantity)))

        unit = parsed_ingredient.amount[0].unit
    else:
        quantity = "0"
        unit = ""

    if quantity == 1 and unit.endswith('s'):
        unit = unit[:-1]

    if parsed_ingredient.sentence is not None:
        sentence = parsed_ingredient.sentence
    else:
        sentence = ''

    if parsed_ingredient.name is not None:
        name = parsed_ingredient.name.text
    else:
        name = ''

    if parsed_ingredient.comment is not None:
        comment = parsed_ingredient.comment.text
    else:
        comment = ''

    if parsed_ingredient.preparation is not None:
        prep = parsed_ingredient.preparation.text
        if (doesStringContainDecimal):
            prep = convert_decimals_to_fractions(prep)
    else:
        prep = ''

    if parsed_ingredient.other is not None:
        other = parsed_ingredient.other.text
    else:
        other = ''

    return {
        'sentence': sentence,
        'name': name,
        'quantity': quantity,
        'unit': unit,
        'comment': comment,
        'preparation': prep,
        'other': other
    }

def put_recipe(recipe):
    cursor.execute(
        insertRecipeSQL,
        [
            recipe.title,
            recipe.source,
            recipe.site_name,
            recipe.url,
            recipe.servings,
            recipe.image,
            recipe.total_time,
            recipe.prep_time,
            recipe.cook_time,
            recipe.calories
        ]
    )
    cursor.connection.commit()

    cursor.execute(
        insertNutritionInfoSQL,
        [
            recipe.recipe_id,
            recipe.calories,
            recipe.total_fat,
            recipe.total_fat_dv,
            recipe.saturated_fat,
            recipe.saturated_fat_dv,
            recipe.carbohydrates,
            recipe.carbohydrates_dv,
            recipe.fiber,
            recipe.fiber_dv,
            recipe.sugar,
            recipe.sugar_dv,
            recipe.protein,
            recipe.protein_dv,
            recipe.cholesterol,
            recipe.cholesterol_dv,
            recipe.sodium,
            recipe.sodium_dv
        ]
    )
    cursor.connection.commit()

    for ingredient in ingredients:
        cursor.execute(
            insertIngredientSQL,
            [
                recipe.recipe_id,
                ingredient["sentence"],
                ingredient["name"],
                ingredient["quantity"],
                ingredient["unit"],
                ingredient["comment"],
                ingredient["other"],
                ingredient["preparation"]
            ]
        )
        cursor.connection.commit()

    for step in steps:
        cursor.execute(
            insertStepSQL,
            [
                recipe.recipe_id,
                step
            ]
        )
        cursor.connection.commit()

    for diet in diets:
        cursor.execute(
            insertDietSQL,
            [
                recipe.recipe_id,
                diet
            ]
        )
        cursor.connection.commit()
    # obj = python_obj_to_dynamo_obj(dictionary)
    # print(json.dumps(obj))
    # client.put_item(
    #     TableName = RECIPE_TABLE,
    #     Item=obj
    # )

#--------------------------------------------

basePage = requests.get(FOOD_NETWORK_URL)
pageTitleList = []
allPages = []
fnList: [str] = []

soup1 = BeautifulSoup(basePage.content, "html.parser")

pages = soup1.find("ul", 'o-IndexPagination__m-List')
pageList = pages.find_all("li", {"class": 'o-IndexPagination__a-ListItem'})
for entry in pageList:
    pageTitleList.append(FOOD_NETWORK_URL + "/" + entry.text.lower().strip())

for page in pageTitleList:
    pageRequest = requests.get(page)
    soup1 = BeautifulSoup(pageRequest.content, "html.parser")
    nums = soup1.find_all("a", {"class": 'o-Pagination__a-Button'})
    lastPageNum = int(nums[len(nums) - 2].text.strip())
    for num in range(1, lastPageNum + 1):
        allPages.append(page + "/p/" + str(num))

if idCount < allPages.__sizeof__():

    # Only scanning 10 recipes
    for page in allPages[idCount: 1]:

        page1 = requests.get(page)

        soup = BeautifulSoup(page1.content, "html.parser")

        newList = []

        listOfPages = soup.find_all("li", {"class": 'm-PromoList__a-ListItem'})
        for entry in listOfPages:
            entry1 = (entry.find('a')["href"]).replace("//", "")
            newList.append(entry1)

        # for index in range(0, len(newList)):
        for index in range(0, 1):
            recipe = Recipe()
            title = ""
            total_time = ""
            prep_time = ""
            cook_time = ""
            servings = ""
            source = ""
            image = ""
            site_name = ""
            url = ""
            calories = -1
            total_fat = -1
            saturated_fat = -1
            carbs = -1
            fiber = -1
            sugar = -1
            protein = -1
            cholesterol = -1  # mg
            sodium = -1  # mg
            ingredients = []
            ingredient_strings = []
            steps = []
            diets = []

            page = requests.get("https://" + newList[index])
            soup1 = BeautifulSoup(page.content, "html.parser")

            # Source
            try:
                if source == "":
                    sourceFull = soup1.find("span", {"class": 'o-Attribution__a-Name'}).text.strip()
                    source = sourceFull.split("of ")[1]
                    print("source: " + source)
            except IndexError:
                print("source index out of range")
            except TypeError:
                print("source type error")
            except AttributeError:
                print("source attribute error")

            try:
                if source == "":
                    sourceFull = soup1.find("span", {"class": 'o-Attribution__a-Name'})
                    source = sourceFull.find("a").text
                    print("source: " + source)
            except IndexError:
                print("source index out of range")
            except TypeError:
                print("source type error")
            except AttributeError:
                print("source attribute error")

            # Site Name
            try:
                if site_name == "":
                    site_name = soup1.find("meta", {"property": 'og:site_name'})["content"].strip()
                    print("site_name: " + site_name)
            except TypeError:
                print("site_name type error")

            if source == "":
                source = site_name

            try:
                if url == "":
                    url = soup1.find("meta", {"property": 'og:url'})["content"].strip()
                    print("url: " + url)
            except TypeError:
                print("url type error")

            try:
                if image == "":
                    image = soup1.find("meta", {"property": 'og:image'})["content"].strip()
                    print("image: " + image)
            except TypeError:
                print("image type error")

            # Title
            try:
                if title == "":
                    title = soup1.find("span", {"class": 'o-AssetTitle__a-HeadlineText'}).text.strip()
                    print("title: " + title)
            except TypeError:
                print("title type error")

            # Total time
            try:
                totalTitle = soup1.find("ul", {"class": 'o-RecipeInfo__m-Time'})
                if totalTitle.find("span",
                                   {"class": 'm-RecipeInfo__a-Description--Total'}) is not None and total_time == "":
                    total_time = totalTitle.find("span", {"class": 'm-RecipeInfo__a-Description--Total'}).text.strip()
                    print("total time: " + total_time)
            except TypeError:
                print("type error")

            for span in soup1.find_all("span", {"class": 'o-RecipeInfo__a-Headline'}):
                text = span.find_next("span", {"class": 'o-RecipeInfo__a-Description'}).text.strip()

                # Servings
                if span.text.lower().__contains__("yield") and servings == "":
                    servings = text
                    print("servings: " + servings)
                # Prep Time
                if span.text.lower().__contains__("prep") and prep_time == "":
                    prep_time = text
                    print("prep_time: " + prep_time)
                # Cook Time
                if span.text.lower().__contains__("cook") and cook_time == "":
                    cook_time = text
                    print("cook_time: " + cook_time)
                # Total Time
                if span.text.lower().__contains__("total") and total_time == "":
                    total_time = text
                    print("total_time: " + total_time)

            # Ingredients
            ingredientInfo = soup1.find_all("span", {"class": 'o-Ingredients__a-Ingredient--CheckboxLabel'})
            for item in ingredientInfo:
                if item.text != "Deselect All":
                    ingredient_strings.append(item.text.strip())
                    print("string: " + item.text.strip())
                    ingredients.append(parse_ingredient_string(item.text.strip()))
                    print("ingredient: " + item.text.strip())

            # Dairy Free
            if DietInfo.isDairyFree(ingredient_strings):
                diets.append(DietInfo.DietType.DAIRY_FREE.value)

            # Vegan
            if DietInfo.isVegan(ingredient_strings):
                diets.append(DietInfo.DietType.VEGAN.value)

            # Gluten Free
            if DietInfo.isGlutenFree(ingredient_strings):
                diets.append(DietInfo.DietType.GLUTEN_FREE.value)

            # Vegetarian
            if DietInfo.isVegetarian(ingredient_strings):
                diets.append(DietInfo.DietType.VEGETARIAN.value)

            # Nut Free
            if DietInfo.isNutFree(ingredient_strings):
                diets.append(DietInfo.DietType.NUT_FREE.value)

            # Steps
            for li in soup1.find_all("li", {"class": 'o-Method__m-Step'}):
                steps.append(li.text.strip())
                print("step: " + li.text.strip())

            # Nutrition
            for dl in soup1.find_all("dl", {"class": 'm-NutritionTable__a-Content'}):
                for dt in dl.find_all_next("dt", {"class": 'm-NutritionTable__a-Headline'}):
                    # Calories
                    if dt.next.strip().lower().__contains__("cal") and calories == -1:
                        caloriesFull = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        if caloriesFull.__contains__(" "):
                            calories = caloriesFull.split(" ")[0].strip()
                        else:
                            calories = caloriesFull
                        print("calories: " + calories)
                    # Total Fat
                    if dt.next.strip().lower().__contains__("total fat") and total_fat == -1:
                        total_fat_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        total_fat = total_fat_full.split("g")[0].strip()
                        print("total fat: " + total_fat)
                    # Saturated Fat
                    if dt.next.strip().lower().__contains__("saturated fat") and saturated_fat == -1:
                        saturated_fat_full = dt.find_next(
                            "dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        saturated_fat = saturated_fat_full.split("g")[0].strip()
                        print("saturated fat: " + saturated_fat)
                    # Carbohydrates
                    if dt.next.strip().lower().__contains__("carbohydrates") and carbs == -1:
                        carbs_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        carbs = carbs_full.split("g")[0].strip()
                        print("carbs: " + carbs)
                    # Dietary Fiber
                    if dt.next.strip().lower().__contains__("dietary fiber") and fiber == -1:
                        fiber_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        fiber = fiber_full.split("g")[0].strip()
                        print("fiber: " + fiber)
                    # Sugar
                    if dt.next.strip().lower().__contains__("sugar") and sugar == -1:
                        sugar_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        sugar = sugar_full.split("g")[0].strip()
                        print("sugar: " + sugar)
                    # Protein
                    if dt.next.strip().lower().__contains__("protein") and protein == -1:
                        protein_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        protein = protein_full.split("g")[0].strip()
                        print("protein: " + protein)
                    # Cholesterol
                    if dt.next.strip().lower().__contains__("cholesterol") and cholesterol == -1:
                        cholesterol_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        cholesterol = cholesterol_full.split("m")[0].strip()
                        print("cholesterol: " + cholesterol)
                    # Sodium
                    if dt.next.strip().lower().__contains__("sodium") and sodium == -1:
                        sodium_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        sodium = sodium_full.split("m")[0].strip()
                        print("sodium: " + sodium)

            # Low Carb
            if DietInfo.isLowCarb(carbs):
                diets.append(DietInfo.DietType.LOW_CARB.value)

            # Low Fat
            if DietInfo.isLowFat(calories, total_fat):
                diets.append(DietInfo.DietType.LOW_FAT.value)

            # Low Sodium
            if DietInfo.isLowSodium(sodium):
                diets.append(DietInfo.DietType.LOW_SODIUM.value)

            # High Protein
            if DietInfo.isHighProtein(calories, protein):
                diets.append(DietInfo.DietType.HIGH_PROTEIN.value)

            # Setting all recipe information
            # ID
            recipe.recipe_id = idCount + 1
            # Title of Recipe
            recipe.title = title
            # Source of Recipe
            if source == "":
                source = site_name
            recipe.source = source
            # Website Name
            recipe.site_name = site_name
            # Servings
            recipe.servings = servings
            # Image
            recipe.image = image
            # Url
            recipe.url = url
            # Total Time
            recipe.total_time = total_time
            # Prep Time
            recipe.prep_time = prep_time
            # Cook Time
            recipe.cook_time = cook_time
            # Nutrition Info
            recipe.calories = int(calories)

            recipe.sodium = int(sodium)
            if sodium != -1:
                recipe.sodium_dv = int((int(sodium) / DV_SODIUM) * 100)
            
            recipe.cholesterol = int(cholesterol)
            if cholesterol != -1:
                recipe.cholesterol_dv = int((int(cholesterol) / DV_CHOLESTEROL) * 100)
            recipe.sugar = int(sugar)
            if sugar != -1:
                recipe.sugar_dv = int((int(sugar) / DV_SUGAR) * 100)
            recipe.fiber = int(fiber)
            if fiber != -1:
                recipe.fiber_dv = int((int(fiber) / DV_FIBER) * 100)
            recipe.protein = int(protein)
            if protein != -1:
                recipe.protein_dv = int((int(protein) / DV_PROTEIN) * 100)
            recipe.total_fat = int(total_fat)
            if total_fat != -1:
                recipe.total_fat_dv = int((int(total_fat) / DV_FAT) * 100)
            recipe.saturated_fat = int(saturated_fat)
            if saturated_fat != -1:
                recipe.saturated_fat_dv = int((int(saturated_fat) / DV_SATURATED_FAT) * 100)
            recipe.carbohydrates = int(carbs)
            if carbs != -1:
                recipe.carbohydrates_dv = int((int(carbs) / DV_CARBS) * 100)
            # Ingredients
            recipe.ingredients = ingredients
            # Steps
            recipe.steps = steps
            # Diets
            recipe.diets = diets

            if recipe.recipe_id == -1 or calories == -1:
                print("something is -1. Skipping the recipe")
            else:
                put_recipe(recipe)
                idCount += 1

else:
    print("idCount ( " + str(idCount) + " )" + " is larger than the number of pages to find ( " +
          str(allPages.__sizeof__()) + " )")

