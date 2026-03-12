import streamlit as st
import random

st.set_page_config(page_title="Weekly Diet Plan", layout="centered")

st.markdown("## Smart Weekly Diet Planner")

goal = st.selectbox("Your Goal", ["weight_loss", "maintenance", "muscle_gain"])

day = st.selectbox(
    "Select Day",
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

all_foods = [
    "Oats","Eggs","Brown rice","White rice","Chapati","Paneer",
    "Chicken","Fish","Dal","Rajma","Poha","Idli","Dosa",
    "Nuts","Fruits","Milk","Curd","Vegetables","Soup"
]

available_foods = st.multiselect("Select Available Foods", all_foods)

def filter_meals(meals, available):
    filtered = []
    for meal in meals:
        for food in available:
            if food.lower() in meal.lower():
                filtered.append(meal)
                break
    return filtered

weight_loss_plan = {
    "breakfast": [
        "Oats with fruits",
        "Boiled eggs",
        "Poha",
        "Idli",
        "Fruit bowl"
    ],
    "lunch": [
        "Brown rice with dal",
        "Chapati with vegetables",
        "Grilled chicken with salad",
        "Rajma with rice"
    ],
    "snack": [
        "Nuts",
        "Fruits",
        "Curd",
        "Boiled corn"
    ],
    "dinner": [
        "Soup with vegetables",
        "Paneer salad",
        "Egg bhurji",
        "Grilled fish"
    ]
}

maintenance_plan = weight_loss_plan
muscle_gain_plan = weight_loss_plan

if goal == "weight_loss":
    plan = weight_loss_plan
elif goal == "maintenance":
    plan = maintenance_plan
else:
    plan = muscle_gain_plan

if st.button("Generate Plan For Selected Day"):

    if not available_foods:
        st.warning("Please select available foods")
    else:
        breakfast_list = filter_meals(plan["breakfast"], available_foods)
        lunch_list = filter_meals(plan["lunch"], available_foods)
        snack_list = filter_meals(plan["snack"], available_foods)
        dinner_list = filter_meals(plan["dinner"], available_foods)

        st.markdown(f"### Plan for {day}")

        if breakfast_list:
            st.write("Breakfast:", random.choice(breakfast_list))
        else:
            st.write("Breakfast: Adjust manually")

        if lunch_list:
            st.write("Lunch:", random.choice(lunch_list))
        else:
            st.write("Lunch: Adjust manually")

        if snack_list:
            st.write("Snack:", random.choice(snack_list))
        else:
            st.write("Snack: Adjust manually")

        if dinner_list:
            st.write("Dinner:", random.choice(dinner_list))
        else:
            st.write("Dinner: Adjust manually")