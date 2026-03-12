import streamlit as st

def apply_style():

    st.markdown("""
    <style>

    .stButton>button {
        height:60px;
        font-size:18px;
        border-radius:10px;
    }

    </style>
    """, unsafe_allow_html=True)