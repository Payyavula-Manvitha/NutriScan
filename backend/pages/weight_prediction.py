import streamlit as st
import pandas as pd
from history import load_history
from health_analysis import calculate_daily_calories

st.set_page_config(page_title="Weight Prediction", layout="centered")

st.title("Monthly Weight Change Prediction")

age = st.number_input("Age", 10, 100, 22)
gender = st.selectbox("Gender", ["male", "female"])
height = st.number_input("Height (cm)", 150)
weight = st.number_input("Weight (kg)", 55)
activity = st.selectbox("Activity Level", ["low", "moderate", "high"])

daily_calories_needed = calculate_daily_calories(
    age, gender, height, weight, activity
)

history = load_history()

if history is None or len(history) == 0:

    st.warning("No meal history available yet.")

else:

    st.subheader("Meal History Used for Prediction")

    st.dataframe(history)

    total_calories = history["Calories"].sum()

    days_logged = len(history)

    expected_calories = daily_calories_needed * days_logged

    calorie_difference = total_calories - expected_calories

    weight_change = calorie_difference / 7700

    st.subheader("Calorie Analysis")

    st.write("Days Logged:", days_logged)
    st.write("Total Calories Consumed:", int(total_calories))
    st.write("Expected Calories:", int(expected_calories))

    st.subheader("Predicted Weight Change")

    if weight_change < 0:

        st.success(
            f"Estimated Weight Loss: {abs(weight_change):.2f} kg"
        )

    elif weight_change > 0:

        st.warning(
            f"Estimated Weight Gain: {weight_change:.2f} kg"
        )

    else:

        st.info("Weight likely stable")

    st.subheader("Calories Trend")

    st.line_chart(history["Calories"])