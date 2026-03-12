def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_daily_calories(age, gender, height, weight, activity):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factor = {"low": 1.2, "moderate": 1.55, "high": 1.725}
    return bmr * activity_factor.get(activity, 1.2)

def generate_health_feedback(total_cal, total_carbs, total_fat, total_protein,
                             goal, diabetes, daily_calories):

    messages = []

    if total_cal > daily_calories * 0.4:
        messages.append(" High calorie meal")

    if goal == "weight_loss" and total_fat > 30:
        messages.append(" Reduce fat intake for weight loss")

    if goal == "muscle_gain" and total_protein < 25:
        messages.append(" Increase protein intake")

    if diabetes and total_carbs > 30:
        messages.append(" High carbs for diabetic profile")

    if not messages:
        messages.append(" Meal fits your health profile")

    return messages
