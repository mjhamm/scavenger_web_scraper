from enum import Enum
from typing import List


class DietType(Enum):
    LOW_CARB = "Low Carb"
    DAIRY_FREE = "Dairy Free"
    HIGH_PROTEIN = "High Protein"
    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"
    LOW_FAT = "Low Fat"
    LOW_SODIUM = "Low Sodium"
    GLUTEN_FREE = "Gluten Free"
    NUT_FREE = "Nut Free"


# TODO: Update and exclude based on nut milks
dairyIngredients = [
    "butter", "cheese", "cream", "custard", "pudding", "ghee", "half & half", "half and half", "1/2 and 1/2",
    "1/2 & 1/2", "casein", "lactalbumin", "Lactoglobulin", "lactoferrin", "lactose", "lactulose", "milk", "nisin",
    "nougat", "recaldent", "rennet", "whey", "yogurt", 'American', 'Asiago', 'Blue Cheese', 'Bocconcini', 'Brie',
    'Burrata', 'Camembert', 'Cheddar', 'Cheese Curds', 'Colby', 'Colby-Jack Cheese', 'Cold-Pack Cheese', 'Cotija',
    'Cottage cheese', 'Cream cheese', 'Emmental', 'Feta', 'Fresh Mozzarella', 'Gorgonzola', 'Gouda', 'Gruyere',
    'Halloumi', 'Havarti', 'Jarlsberg', 'Limburger', 'Mascarpone', 'Monterey Jack', 'Mozzarella', 'Muenster',
    'Neufchatel', 'Paneer', 'Parmesan', 'Pepper Jack', 'Provolone', 'Ricotta', 'Romano', 'String Cheese', 'Swiss',
    'half-and-half', 'half-&-half', '1/2-and-1/2'
]

# TODO: Update and exclude based on nut milks
nutIngredients = [
    'almonds', 'almond', 'Brazil nut', 'Brazil nuts', 'cashew', 'hazelnut', 'macadamia nut', 'pecan', "pine nut",
    'pignolia', 'pistachio nut', 'walnut', 'Peanut', 'cashews', 'hazelnuts', 'macadamia nuts', 'pecans', "pine nuts",
    'pignolias', 'pistachio nuts', 'walnuts', 'Peanuts'
]


def isHighProtein(calories, protein) -> bool:
    try:
        if int(calories) * .3 >= protein:
            return True
        else:
            return False
    except TypeError:
        return False
    except ValueError:
        return False


def isLowSodium(sodium) -> bool:
    try:
        if int(sodium) <= 140:
            return True
        else:
            return False
    except TypeError:
        return False
    except ValueError:
        return False


def isLowFat(calories, fat) -> bool:
    try:
        if int(calories) * .3 <= int(fat):
            return True
        else:
            return False
    except TypeError:
        return False
    except ValueError:
        return False


def isLowCarb(carbs) -> bool:
    try:
        if int(carbs) <= 7:
            return True
        else:
            return False
    except TypeError:
        return False
    except ValueError:
        return False


def isNutFree(ingredients: List[str]) -> bool:
    for ingredient in ingredients:
        for nut in nutIngredients:
            if nut.lower() in ingredient.lower():
                return False
    return True


def isDairyFree(ingredients: List[str]) -> bool:
    for ingredient in ingredients:
        for dairy in dairyIngredients:
            if dairy.lower() in ingredient.lower():
                return False
    return True
