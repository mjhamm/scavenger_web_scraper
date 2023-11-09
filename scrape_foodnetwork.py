import boto3
import requests
import json
from constants import *
import diets as DietInfo
from recipe import Recipe
from bs4 import BeautifulSoup
from decimal import Decimal
from ingredient_parser import parse_ingredient

dynamodb = boto3.resource(service_name = 'dynamodb',region_name = REGION_NAME,
              aws_access_key_id = AWS_ACCESS_KEY,
              aws_secret_access_key = AWS_SECRET_KEY)

recipe_table = dynamodb.Table(RECIPE_TABLE)
recipe_stats_table = dynamodb.Table(RECIPE_STATS_TABLE)

client = boto3.client('dynamodb','us-east-2', aws_access_key_id = AWS_ACCESS_KEY,
              aws_secret_access_key = AWS_SECRET_KEY)

response = client.describe_table(TableName=RECIPE_TABLE)
idCount = response['Table']['ItemCount']

# -- FUNCTIONS -- #

# Parses Ingredient String into separate readable parts
def parse_ingredient_string(ingredient_string) -> dict:
    parsed_ingredient = parse_ingredient(ingredient_string)
    print(parsed_ingredient)

    if len(parsed_ingredient.amount) != 0: 
        quantity = parsed_ingredient.amount[0].quantity
        unit = parsed_ingredient.amount[0].unit
    else:
        quantity = 0
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

# Add item to Recipe Table
def put_recipe(id: int, recipe: Recipe):
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
    for page in allPages[idCount: 30]:

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

            # print("id: " + str(idCount))

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
            recipe.id = idCount + 1
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
            recipe.calories = calories
            recipe.sodium = sodium
            if sodium != -1:
                recipe.dv_sodium = int((int(sodium) / DV_SODIUM) * 100)
            recipe.cholesterol = cholesterol
            if cholesterol != -1:
                recipe.dv_cholesterol = int((int(cholesterol) / DV_CHOLESTEROL) * 100)
            recipe.sugar = sugar
            if sugar != -1:
                recipe.dv_sugar = int((int(sugar) / DV_SUGAR) * 100)
            recipe.fiber = fiber
            if fiber != -1:
                recipe.dv_fiber = int((int(fiber) / DV_FIBER) * 100)
            recipe.protein = protein
            if protein != -1:
                recipe.dv_protein = int((int(protein) / DV_PROTEIN) * 100)
            recipe.total_fat = total_fat
            if total_fat != -1:
                recipe.dv_total_fat = int((int(total_fat) / DV_FAT) * 100)
            recipe.saturated_fat = saturated_fat
            if saturated_fat != -1:
                recipe.dv_saturated_fat = int((int(saturated_fat) / DV_SATURATED_FAT) * 100)
            recipe.carbs = carbs
            if carbs != -1:
                recipe.dv_carbs = int((int(carbs) / DV_CARBS) * 100)
            # Ingredients
            recipe.ingredients = ingredients
            # Steps
            recipe.steps = steps
            # Diets
            recipe.diets = diets

            recipe_json = json.dumps(recipe.__dict__)
            print(recipe_json)
            datadict = json.loads(recipe_json, parse_float=Decimal)

            if recipe.id == -1 or calories == -1:
                print("something is -1. Skipping the recipe")
            else:
                put_recipe(idCount, recipe)

                idCount += 1

else:
    print("idCount ( " + str(idCount) + " )" + " is larger than the number of pages to find ( " +
          str(allPages.__sizeof__()) + " )")

