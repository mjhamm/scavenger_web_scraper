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


glutenFreeIngredients = [
    'Wheat',
    'Barley',
    'Rye',
    'Triticale',
    'Bulgur',
    'Couscous',
    'Semolina',
    'Durum',
    'Spelt',
    'Kamut',
    'Farina',
    'Malt',
    'Bread',
    'Pasta',
    'Cakes',
    'Cookies',
    'cookie',
    'cake',
    'Pastries',
    'pastry',
    'Crackers',
    'cracker'
    'Cereal',
    'Beer',
    'Soy sauce',
    'yeast',
    'Wheat germ',
    'bread',
    'breadcrumbs'
    'Matzo',
    'pretzel'
    'Pretzels',
    'Scones',
    'scone',
    'Waffles',
    'waffle',
    'Pizza crust',
    'Tortilla',
    'tortilla'
    'Pie crusts',
    'pie crust'
    'Biscuits',
    'biscuit',
    'dumpling',
    'Dumplings',
    'Stuffing',
    'Croissants',
    'croissant',
    'naan',
    'bagel',
    'Bagels',
    'Muffins',
    'muffin',
    'Pancakes',
    'pancake',
    'Flour tortillas',
    'flour',
    'Malt vinegar'
]

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

nutIngredients = [
    'almonds', 'almond', 'Brazil nut', 'Brazil nuts', 'cashew', 'hazelnut', 'macadamia nut', 'pecan', "pine nut",
    'pignolia', 'pistachio nut', 'walnut', 'Peanut', 'cashews', 'hazelnuts', 'macadamia nuts', 'pecans', "pine nuts",
    'pignolias', 'pistachio nuts', 'walnuts', 'Peanuts'
]

vegetarianIngredients = [
    'Beef', 'pork', 'lamb', 'meat', 'Chicken', 'duck', 'veal', 'venison', 'ox', 'poultry', 'turkey', 'Fish',
    'shellfish', 'crabs', 'clams', 'mussels', 'scallop', 'scallops', 'anchovies', 'shrimp', 'squid', 'calamari', 'crab',
    'lobster', 'lobsters', 'goose', 'quail', 'bee pollen', 'royal jelly', 'gelatin', 'marshmallow', 'marshmallows',
    'fillet', 'fillets', 'bone', 'bones', 'mackerel', 'Catfish', 'pike', 'Bluegill', 'eels', 'Eel', 'Barramundi',
    'Goldfish', 'Tuna', 'perch', 'Gadidae', 'Walleye', 'Arctic char', 'Bowfin', 'Smelt', 'Burbot', 'Guppy', 'dogfish',
    'Bonefish', 'seabass', 'cod', 'Muskellunge', 'Whiting', 'Stickleback', 'pickerel', 'Haddock', 'trout', 'salmon',
    'bullhead', 'sunfish', 'bass', 'Broth', 'Stock', 'Lard', 'Tallow', 'Suet', 'Rennet', 'Sausage', 'Bacon', 'Ham',
    'Sausages', 'game'
]

veganIngredients = [
    'Mayonnaise', 'honey', 'Casein', 'Whey', 'Ghee', 'Shellac', 'Carmine', 'Lactose', 'Glycerin'
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


def isVegetarian(ingredients: List[str]) -> bool:
    for ingredient in ingredients:
        for vegan in vegetarianIngredients:
            if vegan.lower() in ingredient.lower():
                return False
    return True


def isGlutenFree(ingredients: List[str]) -> bool:
    for ingredient in ingredients:
        for gluten in glutenFreeIngredients:
            if gluten.lower() in ingredient.lower():
                return False
    return True


def isVegan(ingredients: List[str]) -> bool:
    veganIngredients.extend(dairyIngredients)
    veganIngredients.extend(vegetarianIngredients)
    for ingredient in ingredients:
        for vegan in veganIngredients:
            if vegan.lower() in ingredient.lower():
                return False
    return True


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
                if dairy.lower() == "milk" or dairy.lower() == "butter" or dairy.lower() == "cheese":
                    for nut in nutIngredients:
                        if not ingredient.__contains__(nut):
                            return False
                return False
    return True
