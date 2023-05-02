import requests
from recipe import Recipe
from bs4 import BeautifulSoup

foodNetworkURL = "https://www.foodnetwork.com/recipes/recipes-a-z/p/1"
page1 = requests.get(foodNetworkURL)

soup = BeautifulSoup(page1.content, "html.parser")

source = str
website = str
total_time = str
fnList = []
newList = []

listOfPages = soup.find_all("li", {"class": 'm-PromoList__a-ListItem'})
for entry in listOfPages:
    entry1 = (entry.find('a')["href"]).replace("//", "")
    newList.append(entry1)


for index in range(0, 1):
    recipe = Recipe()
    servings = str
    totalTime = str
    ingredients = [str]

    page = requests.get("https://" + newList[index])
    soup1 = BeautifulSoup(page.content, "html.parser")

    # Title
    title = soup1.find("span", {"class": 'o-AssetTitle__a-HeadlineText'}).text

    # Total time
    totalTitle = soup1.find("ul", {"class": 'o-RecipeInfo__m-Time'})
    for li in totalTitle.find("span", {"class": 'o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total'}):
        total_time = li.text

    # Servings
    yieldTitle = soup1.find("ul", {"class": 'o-RecipeInfo__m-Yield'})
    for li in yieldTitle.find("span", {"class": 'o-RecipeInfo__a-Description'}):
        if li.text.__contains__("servings"):
            servings = li.text

    # Ingredients
    ingredientInfo = soup1.find_all("span", {"class": 'o-Ingredients__a-Ingredient--CheckboxLabel'})
    for item in ingredientInfo:
        if item.text == "Deselect All":
            print(item.text)
        else:
            ingredients.append(item)

    # Source and Website
    results = soup1.find("title").text.replace("\"", "").replace("\'", "\"").split("|")

    try:
        source = results[1].rstrip().lstrip()
    except IndexError:
        print("source index error")

    try:
        website = results[2].rstrip().lstrip()
    except IndexError:
        print("website index error")

    # Setting all recipe information
    recipe.id = index
    recipe.title = title
    recipe.source = source
    recipe.servings = servings
    recipe.website = website
    recipe.total_time = total_time
    recipe.ingredients = ingredients

    fnList.append(recipe)
