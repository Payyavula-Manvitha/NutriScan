import streamlit as st
import pandas as pd
import os

FILE_PATH = "meal_history.csv"

# ---------------- LOAD HISTORY ----------------
def load_history():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return None

# ---------------- HEALTH SCORE FUNCTION ----------------
def calculate_health_score(calories, carbs, protein, fat):
    score = 5  # Base score

    if protein > 25:
        score += 2
    if fat > 40:
        score -= 2
    if carbs > 60:
        score -= 1
    if calories < 400:
        score += 1

    return max(1, min(score, 10))

# ---------------- PAGE UI ----------------
st.set_page_config(page_title="Meal Health Score", layout="centered")

st.title(" Meal Health Score Dashboard")

history = load_history()

if history is not None and not history.empty:

    history["Health Score"] = history.apply(
        lambda row: calculate_health_score(
            row["Calories"], row["Carbs"], row["Protein"], row["Fat"]
        ),
        axis=1
    )

    st.subheader(" Recent Meal Scores")
    st.dataframe(history.tail(10))

    st.subheader(" Score Trend")
    st.line_chart(history["Health Score"])

    avg_score = history["Health Score"].mean()

    st.subheader(" Overall Diet Quality")
    st.write(f"Average Meal Health Score: **{avg_score:.1f}/10**")

    if avg_score >= 8:
        st.success("Excellent diet quality! ")
    elif avg_score >= 5:
        st.info("Decent diet, but room for improvement.")
    else:
        st.warning("Diet needs improvement. Try healthier food choices.")
else:
    st.info("No meal history available yet.")
