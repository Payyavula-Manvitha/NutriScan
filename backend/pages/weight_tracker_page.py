import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE_PATH = "weight_history.csv"

# ---------------- FUNCTIONS ----------------
def save_weight(weight):
    data = {
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Weight": [weight]
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(FILE_PATH):
        df_old = pd.read_csv(FILE_PATH)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(FILE_PATH, index=False)

def load_weight_history():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return None

# ---------------- PAGE UI ----------------
st.set_page_config(page_title="Weight Tracker", layout="centered")

st.title(" Weight Progress Tracker")

current_weight = st.number_input("Enter today's weight (kg)", min_value=20.0, max_value=200.0, step=0.1)

if st.button(" Log Weight"):
    save_weight(current_weight)
    st.success("Weight logged successfully!")

st.markdown("---")

history = load_weight_history()

if history is not None and not history.empty:
    st.subheader(" Weight History")
    st.dataframe(history.tail(10))

    st.subheader(" Weight Trend")
    history["Date"] = pd.to_datetime(history["Date"])
    st.line_chart(history.set_index("Date")["Weight"])

    # Weight trend insight
    if len(history) > 1:
        change = history["Weight"].iloc[-1] - history["Weight"].iloc[0]
        if change < 0:
            st.success(f"Great! You have lost {abs(change):.1f} kg ")
        elif change > 0:
            st.warning(f"Weight increased by {change:.1f} kg")
        else:
            st.info("No weight change yet.")
else:
    st.info("No weight records yet. Start logging!")
