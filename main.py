import requests
import csv
from recipe import Recipe
from bs4 import BeautifulSoup

# Food Network
baseFoodNetworkURL = "https://www.foodnetwork.com/recipes/recipes-a-z"

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

for page in allPages[:2]:

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
        calories = None
        total_fat = None
        saturated_fat = None
        carbs = None
        fiber = None
        sugar = None
        protein = None
        cholesterol = None  # mg
        sodium = None  # mg
        ingredients = [str]
        steps = [str]

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
        ingredients.remove(ingredients[0])

        # Steps
        for li in soup1.find_all("li", {"class": 'o-Method__m-Step'}):
            steps.append(li.text.strip())
            print("step: " + li.text.strip())
        steps.remove(steps[0])

        # Nutrition
        for dl in soup1.find_all("dl", {"class": 'm-NutritionTable__a-Content'}):
            for dt in dl.find_all_next("dt", {"class": 'm-NutritionTable__a-Headline'}):
                # Calories
                if dt.next.strip().lower().__contains__("calories") and calories is None:
                    calories = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    print("calories: " + calories)
                # Total Fat
                if dt.next.strip().lower().__contains__("total fat") and total_fat is None:
                    total_fat_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    total_fat = total_fat_full.split("g")[0].strip()
                    print("total fat: " + total_fat)
                # Saturated Fat
                if dt.next.strip().lower().__contains__("saturated fat") and saturated_fat is None:
                    saturated_fat_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    saturated_fat = saturated_fat_full.split("g")[0].strip()
                    print("saturated fat: " + saturated_fat)
                # Carbohydrates
                if dt.next.strip().lower().__contains__("carbohydrates") and carbs is None:
                    carbs_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    carbs = carbs_full.split("g")[0].strip()
                    print("carbs: " + carbs)
                # Dietary Fiber
                if dt.next.strip().lower().__contains__("dietary fiber") and fiber is None:
                    fiber_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    fiber = fiber_full.split("g")[0].strip()
                    print("fiber: " + fiber)
                # Sugar
                if dt.next.strip().lower().__contains__("sugar") and sugar is None:
                    sugar_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    sugar = sugar_full.split("g")[0].strip()
                    print("sugar: " + sugar)
                # Protein
                if dt.next.strip().lower().__contains__("protein") and protein is None:
                    protein_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    protein = protein_full.split("g")[0].strip()
                    print("protein: " + protein)
                # Cholesterol
                if dt.next.strip().lower().__contains__("cholesterol") and cholesterol is None:
                    cholesterol_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    cholesterol = cholesterol_full.split("mg")[0].strip()
                    print("cholesterol: " + cholesterol)
                # Sodium
                if dt.next.strip().lower().__contains__("sodium") and sodium is None:
                    sodium_full = dt.find_next("dd", {"class": 'm-NutritionTable__a-Description'}).next.strip()
                    sodium = sodium_full.split("mg")[0].strip()
                    print("sodium: " + sodium)

        # Setting all recipe information
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

        fnList.append(recipe)

with open('recipes.csv', 'w', ) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'title',
        'source',
        'site_name',
        'url',
        'servings',
        'image',
        'total_time',
        'prep_time',
        'cook_time',
        'calories',
        'total_fat',
        'saturated_fat',
        'carbs',
        'fiber',
        'sugar',
        'protein',
        'cholesterol',
        'sodium',
        'ingredients',
        'steps'
    ])
    for recipe in fnList:
        writer.writerow([
            recipe.title,
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
            recipe.sodium,
            recipe.ingredients,
            recipe.steps
        ])
