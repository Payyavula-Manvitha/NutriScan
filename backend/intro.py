import streamlit as st

def show_intro():

    st.markdown(
        """
        <div style="text-align:center;margin-top:120px">
        <h1 style="font-size:70px;">NutriScan</h1>
        <p style="font-size:22px;">AI Powered Food Scanner and Health Assistant</p>
        </div>
        """,
        unsafe_allow_html=True
    )