import streamlit as st
from database import add_user, login_user


def signup():

    st.title("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    age = st.number_input("Age",10,100)
    height = st.number_input("Height")
    weight = st.number_input("Weight")

    if st.button("Register"):

        add_user(name,email,password,age,height,weight)

        st.success("Account Created")


def login():

    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login_user(email,password)

        if user:

            st.session_state.user = user[1]
            st.session_state.page = "dashboard"

        else:

            st.error("Invalid credentials")