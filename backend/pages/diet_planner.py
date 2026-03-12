import streamlit as st
import random

st.set_page_config(page_title="Weekly Diet Plan", layout="centered")

st.markdown("## Smart Weekly Diet Planner")

condition = st.selectbox(
    "Health Condition",
    [
        "normal",
        "diabetes",
        "weight_loss",
        "weight_gain",
        "heart_patient",
        "high_bp",
        "high_cholesterol"
    ]
)

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


normal_plan = {

    "breakfast":[
        "Oats with milk",
        "Idli with sambar",
        "Poha",
        "Egg omelette",
        "Fruit bowl"
    ],

    "lunch":[
        "Rice with dal",
        "Chapati with vegetables",
        "Rajma with rice",
        "Chicken curry with chapati"
    ],

    "snack":[
        "Nuts",
        "Fruits",
        "Curd"
    ],

    "dinner":[
        "Vegetable soup",
        "Paneer salad",
        "Dal with chapati"
    ]
}


diabetes_plan = {

    "breakfast":[
        "Oats with nuts",
        "Boiled eggs",
        "Vegetable omelette",
        "Sprouts salad"
    ],

    "lunch":[
        "Brown rice with dal",
        "Chapati with vegetables",
        "Grilled fish with salad"
    ],

    "snack":[
        "Nuts",
        "Curd",
        "Sprouts"
    ],

    "dinner":[
        "Vegetable soup",
        "Paneer salad",
        "Grilled chicken"
    ]
}


weight_loss_plan = {

    "breakfast":[
        "Oats with fruits",
        "Boiled eggs",
        "Fruit bowl"
    ],

    "lunch":[
        "Brown rice with vegetables",
        "Chapati with dal",
        "Grilled chicken salad"
    ],

    "snack":[
        "Fruits",
        "Nuts"
    ],

    "dinner":[
        "Vegetable soup",
        "Paneer salad",
        "Grilled fish"
    ]
}


weight_gain_plan = {

    "breakfast":[
        "Milk with oats",
        "Egg omelette with toast",
        "Paneer paratha"
    ],

    "lunch":[
        "Rice with chicken curry",
        "Chapati with paneer curry",
        "Rice with dal and vegetables"
    ],

    "snack":[
        "Milk",
        "Nuts",
        "Banana smoothie"
    ],

    "dinner":[
        "Chicken curry with chapati",
        "Paneer curry with rice"
    ]
}


heart_plan = {

    "breakfast":[
        "Oats with fruits",
        "Vegetable poha",
        "Fruit smoothie"
    ],

    "lunch":[
        "Brown rice with vegetables",
        "Chapati with dal",
        "Vegetable quinoa bowl"
    ],

    "snack":[
        "Fruits",
        "Nuts"
    ],

    "dinner":[
        "Vegetable soup",
        "Steamed vegetables",
        "Paneer salad"
    ]
}


bp_plan = {

    "breakfast":[
        "Oats with banana",
        "Fruit bowl",
        "Vegetable omelette"
    ],

    "lunch":[
        "Brown rice with dal",
        "Chapati with vegetables"
    ],

    "snack":[
        "Fruits",
        "Curd"
    ],

    "dinner":[
        "Vegetable soup",
        "Boiled vegetables"
    ]
}


cholesterol_plan = {

    "breakfast":[
        "Oats with almonds",
        "Fruit bowl",
        "Vegetable smoothie"
    ],

    "lunch":[
        "Brown rice with vegetables",
        "Chapati with dal"
    ],

    "snack":[
        "Nuts",
        "Fruits"
    ],

    "dinner":[
        "Vegetable soup",
        "Steamed vegetables",
        "Paneer salad"
    ]
}


if condition == "normal":
    plan = normal_plan

elif condition == "diabetes":
    plan = diabetes_plan

elif condition == "weight_loss":
    plan = weight_loss_plan

elif condition == "weight_gain":
    plan = weight_gain_plan

elif condition == "heart_patient":
    plan = heart_plan

elif condition == "high_bp":
    plan = bp_plan

else:
    plan = cholesterol_plan


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