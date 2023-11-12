

class Recipe:
    recipe_id: int = -1
    title = ""
    source = ""
    site_name = ""
    url = ""
    servings = ""
    image = ""
    total_time = ""
    prep_time = ""
    cook_time = ""
    calories: int = -1
    total_fat: int = -1
    total_fat_dv: int = -1
    saturated_fat: int = -1
    saturated_fat_dv: int = -1
    carbohydrates: int = -1
    carbohydrates_dv: int = -1
    fiber: int = -1
    fiber_dv: int = -1
    sugar: int = -1
    sugar_dv: int = -1
    protein: int = -1
    protein_dv: int = -1
    cholesterol: int = -1
    cholesterol_dv: int = -1
    sodium: int = -1
    sodium_dv: int = -1
    ingredients: {}
    steps: []
    diets: []
