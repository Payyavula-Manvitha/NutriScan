NUTRITION_DB = {
    # Indian
    "samosa": {"cal": 260, "carbs": 30, "protein": 6, "fat": 14},
    "biriyani": {"cal": 180, "carbs": 22, "protein": 6, "fat": 7},
    "dosa": {"cal": 170, "carbs": 28, "protein": 4, "fat": 4},
    "idli": {"cal": 140, "carbs": 30, "protein": 4, "fat": 1},
    "rajma": {"cal": 140, "carbs": 24, "protein": 9, "fat": 2},
    "gulab_jamun": {"cal": 150, "carbs": 20, "protein": 2, "fat": 6},

    # Fruits
    "apple": {"cal": 52, "carbs": 14, "protein": 0.3, "fat": 0.2},
    "banana": {"cal": 89, "carbs": 23, "protein": 1.1, "fat": 0.3},
    "orange": {"cal": 47, "carbs": 12, "protein": 0.9, "fat": 0.1},
    "grape": {"cal": 69, "carbs": 18, "protein": 0.7, "fat": 0.2},
    "peach": {"cal": 39, "carbs": 10, "protein": 0.9, "fat": 0.3},
    "strawberry": {"cal": 32, "carbs": 8, "protein": 0.7, "fat": 0.3},

    # Western foods
    "pizza": {"cal": 266, "carbs": 33, "protein": 11, "fat": 10},
    "hamburger": {"cal": 295, "carbs": 30, "protein": 17, "fat": 13},
    "sandwich": {"cal": 250, "carbs": 30, "protein": 12, "fat": 8},
    "pasta": {"cal": 131, "carbs": 25, "protein": 5, "fat": 1.1},
    "sushi": {"cal": 130, "carbs": 28, "protein": 6, "fat": 2},
    "cake": {"cal": 257, "carbs": 38, "protein": 3.6, "fat": 10},

    # Veggies
    "salad": {"cal": 33, "carbs": 6, "protein": 2, "fat": 0.4},
    "tomato": {"cal": 18, "carbs": 3.9, "protein": 0.9, "fat": 0.2},
    "cucumber": {"cal": 16, "carbs": 3.6, "protein": 0.5, "fat": 0.1},
}

PORTION_REFERENCE = {
    "pizza": 200,
    "sushi": 150,
    "burger": 180,
    "cake": 120,
    "banana": 120,
    "apple": 150,
    "orange": 130,
    "peach": 150,
    "strawberry": 100,
    "samosa": 100,
}

def estimate_portion(food, box_area, img_area):
    base = PORTION_REFERENCE.get(food, 150)
    ratio = box_area / img_area
    if ratio < 0.1:
        return base * 0.5
    elif ratio < 0.25:
        return base
    else:
        return base * 1.5

def calculate_nutrition(food, grams):
    nut = NUTRITION_DB.get(food, {"cal":100,"carbs":10,"protein":5,"fat":5})
    factor = grams / 100
    return {
        "calories": nut["cal"] * factor,
        "carbs": nut["carbs"] * factor,
        "protein": nut["protein"] * factor,
        "fat": nut["fat"] * factor
    }
