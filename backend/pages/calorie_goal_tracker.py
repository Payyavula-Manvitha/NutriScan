import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from history import load_history
from health_analysis import calculate_daily_calories

st.title(" Weekly Calorie Goal Tracker")

history = load_history()

if history is None or history.empty:
    st.warning("No meal history yet.")
else:
    # ---------- FIX FOR YOUR ERROR ----------
    if "Date" not in history.columns:
        st.info("Old meal history detected. Creating dates automatically.")
        history["Date"] = pd.date_range(end=datetime.today(), periods=len(history))

    history["Date"] = pd.to_datetime(history["Date"])

    # ---------- USER PROFILE INPUT ----------
    st.sidebar.header("Profile for Goal Calculation")
    age = st.sidebar.number_input("Age", 1, 100, 20)
    gender = st.sidebar.selectbox("Gender", ["male", "female"])
    height = st.sidebar.number_input("Height (cm)", 150)
    weight = st.sidebar.number_input("Weight (kg)", 55)
    activity = st.sidebar.selectbox("Activity Level", ["low", "moderate", "high"])

    daily_need = calculate_daily_calories(age, gender, height, weight, activity)
    weekly_goal = daily_need * 7

    last_week = history[history["Date"] > datetime.now() - timedelta(days=7)]
    weekly_consumed = last_week["Calories"].sum()

    remaining = weekly_goal - weekly_consumed
    progress = min(100, (weekly_consumed / weekly_goal) * 100)

    st.subheader(" Weekly Progress")
    st.write(f" Goal: {weekly_goal:.0f} kcal")
    st.write(f" Consumed: {weekly_consumed:.0f} kcal")
    st.write(f" Remaining: {remaining:.0f} kcal")

    st.progress(int(progress))

    st.subheader(" Daily Intake Trend")
    st.line_chart(last_week.set_index("Date")["Calories"])
