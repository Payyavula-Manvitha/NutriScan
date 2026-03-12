import streamlit as st
import sqlite3
import pandas as pd
from history import load_history

st.title("Admin Panel")

if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# Only admin email allowed
ADMIN_EMAIL = "admin@nutriscan.com"

if st.session_state.email != ADMIN_EMAIL:
    st.error("Access denied. Admin only.")
    st.stop()

st.subheader("Registered Users")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT name, email, age, height, weight FROM users")
users = cursor.fetchall()

if users:
    df = pd.DataFrame(users, columns=["Name", "Email", "Age", "Height", "Weight"])
    st.dataframe(df)
    st.metric("Total Users", len(df))
else:
    st.write("No users registered yet")

st.divider()

st.subheader("Meal Logs")

history = load_history()

if history is not None:
    st.dataframe(history)
    st.metric("Total Meals Logged", len(history))

    st.subheader("Calories Trend")
    st.line_chart(history["Calories"])
else:
    st.write("No meals logged yet")