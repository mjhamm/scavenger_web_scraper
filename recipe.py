

class Recipe:
    id: int = -1
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
    dv_total_fat: int = -1
    saturated_fat: int = -1
    dv_saturated_fat: int = -1
    carbs: int = -1
    dv_carbs: int = -1
    fiber: int = -1
    dv_fiber: int = -1
    sugar: int = -1
    dv_sugar: int = -1
    protein: int = -1
    dv_protein: int = -1
    cholesterol: int = -1
    dv_cholesterol: int = -1
    sodium: int = -1
    dv_sodium: int = -1
    ingredients: {}
    steps: []
    diets: []
