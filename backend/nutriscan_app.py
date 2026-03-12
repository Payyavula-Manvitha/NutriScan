import streamlit as st
import numpy as np
import torch
import matplotlib.pyplot as plt
import os
from ultralytics import YOLO
from torchvision import models, transforms
from PIL import Image

from nutrition import calculate_nutrition, estimate_portion, NUTRITION_DB
from health_analysis import calculate_bmi, bmi_status, calculate_daily_calories, generate_health_feedback
from history import save_meal, load_history
from database import add_user, login_user
from login_streak import save_login, calculate_streak


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

st.set_page_config(page_title="NutriScan", layout="centered")


# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "email" not in st.session_state:
    st.session_state.email = ""


# LOGIN PAGE
if not st.session_state.logged_in:

    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;margin-top:120px'>
    <h1 style='font-size:60px;'>NutriScan</h1>
    <p style='font-size:22px;'>AI Powered Food Scanner and Health Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login","Sign Up"])


    # LOGIN
    with tab1:

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if email == "admin@nutriscan.com" and password == "admin123":

                save_login()

                st.session_state.logged_in = True
                st.session_state.user = "Admin"
                st.session_state.email = email
                st.rerun()


            user = login_user(email,password)

            if user:

                save_login()

                st.session_state.logged_in = True
                st.session_state.user = user[1]
                st.session_state.email = email
                st.rerun()

            else:
                st.error("Invalid credentials")


    # SIGNUP
    with tab2:

        name = st.text_input("Name")
        email_signup = st.text_input("Email", key="signup_email")
        password_signup = st.text_input("Password", type="password", key="signup_pass")
        age_signup = st.number_input("Age",10,100)
        height_signup = st.number_input("Height")
        weight_signup = st.number_input("Weight")

        if st.button("Create Account"):

            add_user(name,email_signup,password_signup,age_signup,height_signup,weight_signup)
            st.success("Account created. Please login.")


    st.stop()



# SIDEBAR
st.sidebar.write("Logged in as:", st.session_state.user)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.session_state.email = ""
    st.rerun()



# UI STYLE
st.markdown("""
<style>
.big-title { font-size:38px; font-weight:700; text-align:center; color:#2E8B57; }
.section { font-size:22px; font-weight:600; margin-top:25px; }
.card { padding:15px; border-radius:12px; background:#1e1e1e; border:1px solid #333; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)



st.markdown('<div class="big-title">NutriScan — Smart Food & Health Analyzer</div>', unsafe_allow_html=True)



# STREAK DISPLAY
current,longest,month = calculate_streak()

st.markdown("### Your Progress")

col1,col2,col3 = st.columns(3)

col1.metric(" Current Streak",current)
col2.metric(" Longest Streak",longest)
col3.metric(" Days This Month",month)



# HEALTH PROFILE
st.sidebar.header("Your Health Profile")

age = st.sidebar.number_input("Age", 1, 100, 20)
gender = st.sidebar.selectbox("Gender", ["male", "female"])
height = st.sidebar.number_input("Height (cm)", 150)
weight = st.sidebar.number_input("Weight (kg)", 55)
activity = st.sidebar.selectbox("Activity Level", ["low", "moderate", "high"])
goal = st.sidebar.selectbox("Goal", ["weight_loss", "maintenance", "muscle_gain"])
diabetes = st.sidebar.checkbox("Diabetes")



# LOAD MODELS
yolo_indian = YOLO(os.path.join(MODEL_DIR, "indian_detector.pt"))

classifier = models.mobilenet_v2(weights=None)
classifier.classifier[1] = torch.nn.Linear(classifier.last_channel, 30)
classifier.load_state_dict(torch.load(os.path.join(MODEL_DIR, "food_classifier.pth"), map_location="cpu"))
classifier.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])



INDIAN_CLASSES = [
"aloo_gobi","aloo_matar","bhature","bhindi_masala","biriyani","chai",
"chole","coconut_chutney","dal","dosa","aloo_dum","fish_curry","ghevar",
"green_chutney","gulab_jamun","idli","jalebi","kebab","kheer","kulfi",
"lassi","mutton_gravy","onion_bhaji","palak_paneer","poha","rajma",
"rasmalai","samosa","shahi_paneer","rice"
]



# IMAGE INPUT
st.markdown("### Select Image Source")

source = st.radio("Choose Input Method", ["Upload Image", "Take Photo"])

image = None

if source == "Upload Image":

    uploaded_file = st.file_uploader("Upload Food Image", type=["jpg","png","jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

else:

    camera_photo = st.camera_input("Take a photo")

    if camera_photo:
        image = Image.open(camera_photo).convert("RGB")



# FOOD DETECTION
if image is not None:

    img = np.array(image)
    img_area = img.shape[0] * img.shape[1]

    results_indian = yolo_indian(img)[0]

    total_cal = total_carbs = total_protein = total_fat = 0

    st.markdown("### Detected Foods")


    for box in results_indian.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        crop = img[y1:y2, x1:x2]

        pil_img = Image.fromarray(crop)
        tensor = transform(pil_img).unsqueeze(0)

        with torch.no_grad():
            probs = torch.softmax(classifier(tensor), dim=1)
            conf, pred = torch.max(probs, 1)

        if conf.item() < 0.5:
            continue


        food = INDIAN_CLASSES[pred.item()]

        grams = estimate_portion(food,(x2-x1)*(y2-y1),img_area)

        nut = calculate_nutrition(food,grams)

        total_cal += nut["calories"]
        total_carbs += nut["carbs"]
        total_protein += nut["protein"]
        total_fat += nut["fat"]


        st.write(food.capitalize(), "-", round(nut["calories"],1), "kcal")


    st.image(image)


    st.markdown("### Meal Summary")

    st.write("Calories:",round(total_cal,1))
    st.write("Carbs:",round(total_carbs,1))
    st.write("Protein:",round(total_protein,1))
    st.write("Fat:",round(total_fat,1))



    # HEALTH INSIGHTS
    bmi = calculate_bmi(weight,height)
    status = bmi_status(bmi)

    daily_cal = calculate_daily_calories(age,gender,height,weight,activity)

    st.markdown("### Personalized Health Insights")

    st.write("BMI:",round(bmi,2),"(",status,")")
    st.write("Daily Calorie Need:",int(daily_cal))


    feedback = generate_health_feedback(
        total_cal,
        total_carbs,
        total_fat,
        total_protein,
        goal,
        diabetes,
        daily_cal
    )


    for msg in feedback:
        st.write(msg)



    if st.button("Save This Meal"):
        save_meal(total_cal,total_carbs,total_protein,total_fat)
        st.success("Meal saved.")



# MEAL HISTORY
st.markdown("### Meal History")

history = load_history()

if history is not None:
    st.dataframe(history.tail(10))
    st.line_chart(history["Calories"])
else:
    st.info("No meal history yet.")