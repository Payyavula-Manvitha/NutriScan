def health_warnings(user, meal_nutrition):
    warnings = []

    if "diabetes" in user.conditions:
        if meal_nutrition["carbs"] > 60:
            warnings.append("⚠ High carbohydrate meal – not ideal for diabetes")

    if "hypertension" in user.conditions:
        warnings.append(" Reduce salty and fried foods")

    if user.goal == "weight_loss":
        if meal_nutrition["calories"] > 600:
            warnings.append(" High calorie meal for weight loss goal")

    return warnings
