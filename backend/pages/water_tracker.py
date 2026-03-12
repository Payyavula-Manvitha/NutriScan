import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE_PATH = "water_log.csv"

# ---------------- SAVE WATER ----------------
def save_water(amount):
    data = pd.DataFrame([[datetime.now().date(), amount]], columns=["Date", "Water(ml)"])
    if os.path.exists(FILE_PATH):
        data.to_csv(FILE_PATH, mode='a', header=False, index=False)
    else:
        data.to_csv(FILE_PATH, index=False)

# ---------------- LOAD WATER ----------------
def load_water():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return None

# ---------------- PAGE UI ----------------
st.set_page_config(page_title="Water Tracker", layout="centered")

st.title(" Daily Water Intake Tracker")

st.write("Track your hydration level throughout the day")

amount = st.number_input("Enter water consumed (ml)", min_value=50, max_value=2000, step=50)

if st.button("Add Water Intake"):
    save_water(amount)
    st.success("Water intake logged!")

data = load_water()

if data is not None:
    st.subheader(" Today's Hydration")

    today = str(datetime.now().date())
    today_data = data[data["Date"] == today]

    total_today = today_data["Water(ml)"].sum()

    goal = 2500  # daily recommended intake

    st.write(f" Water consumed today: **{total_today} ml**")
    st.write(f" Daily goal: **{goal} ml**")

    progress = min(100, int((total_today / goal) * 100))
    st.progress(progress)

    if total_today >= goal:
        st.success("Great hydration today! ")
    else:
        st.warning("Drink more water to stay hydrated!")

    st.subheader(" Water Intake Trend")
    daily_sum = data.groupby("Date")["Water(ml)"].sum()
    st.line_chart(daily_sum)
else:
    st.info("No water data recorded yet.")
