import requests
import csv
import pymysql
import os
import boto3
import json
from botocore.exceptions import ClientError
import diets as DietInfo
from recipe import Recipe
from bs4 import BeautifulSoup

ENDPOINT = 'scavenger.cafbhjmtde7x.us-east-2.rds.amazonaws.com'
PORT = '3306'
USER = 'admin'
PASSWORD = '$94RdsPass394'
REGION = "us-east-2c"
DBNAME = 'scavenger'

connection = pymysql.connect(
    host=ENDPOINT,
    user=USER,
    password=PASSWORD,
    database=DBNAME
)

insertRecipeSQL = """INSERT INTO recipes (title, source, site_name, url, servings, image, total_time, prep_time,
cook_time, calories, total_fat, saturated_fat, carbs, fiber, sugar, protein, cholesterol, sodium)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    """

cursor = connection.cursor()

cursor.execute("select count(*) from recipes")
idCount: int = cursor.fetchone()[0]

# Food Network
baseFoodNetworkURL = "https://www.foodnetwork.com/recipes/recipes-a-z"

# idCount: int = recipe_table.item_count

# All Recipes
# baseAllRecipesURL = "https://www.allrecipes.com/recipes-a-z-6735880"
#
basePage = requests.get(baseFoodNetworkURL)
pageTitleList = []
allPages = []
fnList: [str] = []

soup1 = BeautifulSoup(basePage.content, "html.parser")

pages = soup1.find("ul", 'o-IndexPagination__m-List')
pageList = pages.find_all("li", {"class": 'o-IndexPagination__a-ListItem'})
for entry in pageList:
    pageTitleList.append(baseFoodNetworkURL + "/" + entry.text.lower().strip())

for page in pageTitleList:
    pageRequest = requests.get(page)
    soup1 = BeautifulSoup(pageRequest.content, "html.parser")
    nums = soup1.find_all("a", {"class": 'o-Pagination__a-Button'})
    lastPageNum = int(nums[len(nums) - 2].text.strip())
    for num in range(1, lastPageNum + 1):
        allPages.append(page + "/p/" + str(num))
if idCount < allPages.__sizeof__():

    # Only scanning 10 recipes
    for page in allPages[idCount: 20]:

        page1 = requests.get(page)

        soup = BeautifulSoup(page1.content, "html.parser")

        newList = []

        listOfPages = soup.find_all("li", {"class": 'm-PromoList__a-ListItem'})
        for entry in listOfPages:
            entry1 = (entry.find('a')["href"]).replace("//", "")
            newList.append(entry1)

        # for index in range(0, len(newList)):
        for index in range(0, len(newList)):
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
            if title == "":
                title = soup1.find("span", {"class": 'o-AssetTitle__a-HeadlineText'}).text.strip()
                print("title: " + title)

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
                    ingredients.append(item.text.strip())
                    print("ingredient: " + item.text.strip())

            # Dairy Free
            if DietInfo.isDairyFree(ingredients):
                diets.append(DietInfo.DietType.DAIRY_FREE.value)

            # Vegan
            if DietInfo.isVegan(ingredients):
                diets.append(DietInfo.DietType.VEGAN.value)

            # Gluten Free
            if DietInfo.isGlutenFree(ingredients):
                diets.append(DietInfo.DietType.GLUTEN_FREE.value)

            # Vegetarian
            if DietInfo.isVegetarian(ingredients):
                diets.append(DietInfo.DietType.VEGETARIAN.value)

            # Nut Free
            if DietInfo.isNutFree(ingredients):
                diets.append(DietInfo.DietType.NUT_FREE.value)

            # Steps
            for li in soup1.find_all("li", {"class": 'o-Method__m-Step'}):
                steps.append(li.text.strip())
                print("step: " + li.text.strip())

            # Nutrition
            # TODO: Strip out only numbers
            for dl in soup1.find_all("dl", {"class": 'm-NutritionTable__a-Content'}):
                for dt in dl.find_all_next("dt", {"class": 'm-NutritionTable__a-Headline'}):
                    # Calories
                    if dt.next.strip().lower().__contains__("calories") and calories == -1:
                        calories = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        print("calories: " + calories)
                    # Total Fat
                    if dt.next.strip().lower().__contains__("total fat") and total_fat == -1:
                        total_fat_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                        total_fat = total_fat_full.split("g")[0].strip()
                        print("total fat: " + total_fat)
                    # Saturated Fat
                    if dt.next.strip().lower().__contains__("saturated fat") and saturated_fat == -1:
                        saturated_fat_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
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
            # recipe.id = idCount
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
            recipe.cholesterol = cholesterol
            recipe.sugar = sugar
            recipe.fiber = fiber
            recipe.protein = protein
            recipe.total_fat = total_fat
            recipe.saturated_fat = saturated_fat
            recipe.carbs = carbs
            # Ingredients
            recipe.ingredients = ingredients
            # Steps
            recipe.steps = steps
            # Diets
            recipe.diets = diets

            recipe_json = json.dumps(recipe.__dict__)
            print(recipe_json)
            datadict = json.loads(recipe_json)

            # idCount += 1

            # if recipe.id == -1:
            #     print("id == -1")
            # else:
            cursor.execute(
                insertRecipeSQL,
                [recipe.title,
                 recipe.source,
                 recipe.site_name,
                 recipe.url,
                 recipe.servings,
                 recipe.image,
                 recipe.total_time,
                 recipe.prep_time,
                 recipe.cook_time,
                 recipe.calories,
                 recipe.total_fat,
                 recipe.saturated_fat,
                 recipe.carbs,
                 recipe.fiber,
                 recipe.sugar,
                 recipe.protein,
                 recipe.cholesterol,
                 recipe.sodium]
            )
            cursor.connection.commit()

            fnList.append(recipe)
    else:
        print("idCount ( " + str(idCount) + " )" + " is larger than the number of pages to find ( " +
              str(allPages.__sizeof__()) + " )")

# with open('recipes.csv', 'w', ) as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow([
#         'title',
#         'source',
#         'site_name',
#         'url',
#         'servings',
#         'image',
#         'total_time',
#         'prep_time',
#         'cook_time',
#         'calories',
#         'total_fat',
#         'saturated_fat',
#         'carbs',
#         'fiber',
#         'sugar',
#         'protein',
#         'cholesterol',
#         'sodium',
#         'ingredients',
#         'steps',
#         'diets'
#     ])
#     for recipe in fnList:
#         writer.writerow([
#             recipe.title,
#             recipe.source,
#             recipe.site_name,
#             recipe.url,
#             recipe.servings,
#             recipe.image,
#             recipe.total_time,
#             recipe.prep_time,
#             recipe.cook_time,
#             recipe.calories,
#             recipe.total_fat,
#             recipe.saturated_fat,
#             recipe.carbs,
#             recipe.fiber,
#             recipe.sugar,
#             recipe.protein,
#             recipe.cholesterol,
#             recipe.sodium,
#             recipe.ingredients,
#             recipe.steps,
#             recipe.diets
#         ])

# basePage = requests.get(baseAllRecipesURL)
# soup1 = BeautifulSoup(basePage.content, "html.parser")
# allRecipesList: [str] = []
# letterList = []
# pagesList = []
#
# for link in soup1.find_all("a", {"class": 'link-list__link type--dog-bold type--dog-link'}):
#     pagesList.append(link['href'])

# for entry in pagesList[:1]:
#
#     page1 = requests.get(entry)
#
#     soup = BeautifulSoup(page1.content, "html.parser")
#
#     newList = []
#
#     for link in soup.find_all("a", {"class": 'comp card--image-top mntl-card-list-items mntl-document-card mntl-card card card--no-image'}):
#         newList.append(link['href'])
#     for link in soup.find_all("a", {"class": 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'}):
#         newList.append(link['href'])
#
#     # Individual urls
#     for item in newList[:1]:
#         page = requests.get(item)
#         soup = BeautifulSoup(page.content, "html.parser")
#
#         print(soup.prettify())

# with open('recipes.csv', 'w', ) as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow([
#         'title',
#         'source',
#         'site_name',
#         'url',
#         'servings',
#         'image',
#         'total_time',
#         'prep_time',
#         'cook_time',
#         'calories',
#         'total_fat',
#         'saturated_fat',
#         'carbs',
#         'fiber',
#         'sugar',
#         'protein',
#         'cholesterol',
#         'sodium',
#         'ingredients',
#         'steps',
#         'diets'
#     ])
#     for recipe in bbcList:
#         writer.writerow([
#             recipe.title,
#             recipe.source,
#             recipe.site_name,
#             recipe.url,
#             recipe.servings,
#             recipe.image,
#             recipe.total_time,
#             recipe.prep_time,
#             recipe.cook_time,
#             recipe.calories,
#             recipe.total_fat,
#             recipe.saturated_fat,
#             recipe.carbs,
#             recipe.fiber,
#             recipe.sugar,
#             recipe.protein,
#             recipe.cholesterol,
#             recipe.sodium,
#             recipe.ingredients,
#             recipe.steps,
#             recipe.diets
#         ])
