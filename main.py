import requests
from bs4 import BeautifulSoup

foodNetworkURL = "https://www.foodnetwork.com/recipes/recipes-a-z/p/1"
page1 = requests.get(foodNetworkURL)

soup = BeautifulSoup(page1.content, "html.parser")

listOfPages = soup.find_all("li", {"class": 'm-PromoList__a-ListItem'})
newList = []
for entry in listOfPages:
    entry1 = (entry.find('a')["href"]).replace("//", "")
    newList.append(entry1)

# print(newList)

fnList = []


class Recipe:
    id: int
    title: str
    source: str
    website: str


for index in range(0, len(newList), 10):
    recipe = Recipe()
    print("https://" + newList[index])
    page = requests.get("https://" + newList[index])
    soup1 = BeautifulSoup(page.content, "html.parser")

    title = soup1.find("span", {"class": 'o-AssetTitle__a-HeadlineText'}).text

    results = soup1.find("title").text.replace("\"", "").replace("\'", "\"").split("|")
    source = results[1].rstrip().lstrip()
    website = results[2].rstrip().lstrip()
    recipe.id = index
    recipe.title = title
    recipe.source = source
    recipe.website = website

    fnList.append(recipe)

print(fnList)
