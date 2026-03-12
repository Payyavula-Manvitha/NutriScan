def calculate_bmr(user):
    if user.gender.lower() == "male":
        return 10 * user.weight_kg + 6.25 * user.height_cm - 5 * user.age + 5
    else:
        return 10 * user.weight_kg + 6.25 * user.height_cm - 5 * user.age - 161


def activity_multiplier(level):
    return {
        "low": 1.2,
        "moderate": 1.55,
        "high": 1.725
    }.get(level, 1.2)


def daily_calories(user):
    bmr = calculate_bmr(user)
    return round(bmr * activity_multiplier(user.activity_level), 2)
