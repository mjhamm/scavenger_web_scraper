import requests
from recipe import Recipe
from bs4 import BeautifulSoup

foodNetworkURL = "https://www.foodnetwork.com/recipes/recipes-a-z/p/1"
page1 = requests.get(foodNetworkURL)

soup = BeautifulSoup(page1.content, "html.parser")

source = ""
website = ""
total_time = ""
prep_time = ""
cook_time = ""
fnList = []
newList = []

listOfPages = soup.find_all("li", {"class": 'm-PromoList__a-ListItem'})
for entry in listOfPages:
    entry1 = (entry.find('a')["href"]).replace("//", "")
    newList.append(entry1)

for index in range(0, 1):
    recipe = Recipe()
    servings = ""
    ingredients = [str]
    steps = [str]

    page = requests.get("https://www.foodnetwork.com/recipes/221-meat-loaf-recipe-1940945")
    # page = requests.get("https://" + newList[index])
    soup1 = BeautifulSoup(page.content, "html.parser")

    # Source and Website
    results = soup1.find("title").text.replace("\"", "").replace("\'", "\"").split("|")

    # Source
    if source == "":
        try:
            sourceFull = soup1.find("span", {"class": 'o-Attribution__a-Name'}).text.lstrip().rstrip()
            source = sourceFull.split("of ")[1]
            print("source:" + source)
        except TypeError:
            print("source type error")

    try:
        website = results[2].rstrip().lstrip()
        print("website: " + website)
    except IndexError:
        print("website index error")

    # Title
    title = soup1.find("span", {"class": 'o-AssetTitle__a-HeadlineText'}).text
    print("title: " + title)

    # Total time
    totalTitle = soup1.find("ul", {"class": 'o-RecipeInfo__m-Time'})
    try:
        for li in totalTitle.find("span", {"class": 'm-RecipeInfo__a-Description--Total'}):
            total_time = li.text.lstrip().rstrip()
            print("total_time: " + total_time + "1")
    except TypeError:
        print("type error")

    for span in soup1.find_all("span", {"class": 'o-RecipeInfo__a-Headline'}):
        # Servings
        if span.text.__contains__("servings"):
            if servings == "":
                servings = span.text.lstrip().rstrip()
                print("servings: " + servings)
        # Prep Time
        if span.text.lower().__contains__("prep"):
            if prep_time == "":
                prep_time = span.find_next("span", {"class": 'o-RecipeInfo__a-Description'}).text.lstrip().rstrip()
                print("prep_time: " + prep_time)
        # Cook Time
        if span.text.lower().__contains__("cook"):
            if cook_time == "":
                cook_time = span.find_next("span", {"class": 'o-RecipeInfo__a-Description'}).text.lstrip().rstrip()
                print("cook_time: " + cook_time)
        # Total Time
        if span.text.lower().__contains__("total"):
            if total_time == "":
                total_time = span.find_next("span", {"class": 'o-RecipeInfo__a-Description'}).text.lstrip().rstrip()
                print("total_time: " + total_time)

    # Ingredients
    ingredientInfo = soup1.find_all("span", {"class": 'o-Ingredients__a-Ingredient--CheckboxLabel'})
    for item in ingredientInfo:
        if item.text != "Deselect All":
            ingredients.append(item.text)
            print("ingredient: " + item.text)

    # Steps
    for li in soup1.find_all("li", {"class": 'o-Method__m-Step'}):
        steps.append(li.text.lstrip().rstrip())
        print("step: " + li.text.lstrip().rstrip())

    # Setting all recipe information
    recipe.id = index
    recipe.title = title
    recipe.source = source
    recipe.servings = servings
    recipe.website = website
    recipe.total_time = total_time
    recipe.prep_time = prep_time
    recipe.cook_time = cook_time
    recipe.ingredients = ingredients

    fnList.append(recipe)
