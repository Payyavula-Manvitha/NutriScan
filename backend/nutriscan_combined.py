import streamlit as st
import numpy as np
from ultralytics import YOLO
from PIL import Image
import cv2

from nutrition import (
    estimate_portion,
    calculate_nutrition,
    INDIAN_CLASSES,
    OPENFOOD_CLASSES,
)

model_indian = YOLO("models/indian.pt")
model_open = YOLO("models/openfood.pt")

st.set_page_config(page_title="NutriScan", layout="centered")
st.title(" NutriScan – AI Food Nutrition Analyzer")

st.header(" User Profile")

age = st.number_input("Age", 1, 100, 20)
gender = st.selectbox("Gender", ["male", "female"])
height = st.number_input("Height (cm)", value=155)
weight = st.number_input("Weight (kg)", value=58)
activity = st.selectbox("Activity Level", ["low", "moderate", "high"])
goal = st.selectbox("Goal", ["weight_loss", "muscle_gain", "maintenance"])
diabetes = st.checkbox("Diabetes")

def calculate_bmr():
    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161

activity_factor = {"low": 1.2, "moderate": 1.55, "high": 1.725}
daily_calories = calculate_bmr() * activity_factor[activity]

st.header("📷 Upload Food Image")
uploaded_file = st.file_uploader("Upload food image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    annotated_img = image_np.copy()

    img_h, img_w, _ = image_np.shape
    img_area = img_h * img_w

    results_indian = model_indian(image_np)[0]
    results_open = model_open(image_np)[0]
    all_results = [("indian", results_indian), ("open", results_open)]

    st.header(" Detected Foods")

    total_cal = total_carbs = total_protein = total_fat = 0
    detected_foods = set()

    for source, results in all_results:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if source == "indian" and conf < 0.4:
                continue
            if source == "open" and conf < 0.6:
                continue

            if source == "indian":
                food_name = INDIAN_CLASSES[cls_id]
            else:
                food_name = OPENFOOD_CLASSES[cls_id]

            if food_name in detected_foods:
                continue

            detected_foods.add(food_name)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            box_area = (x2 - x1) * (y2 - y1)

            grams = estimate_portion(food_name, box_area, img_area)
            nutrition = calculate_nutrition(food_name, grams)

            # Draw bounding box
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(
                annotated_img,
                food_name.replace('_',' '),
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            st.subheader(f" {food_name.replace('_',' ').title()}")
            st.write(f"Confidence: **{conf:.2f}**")
            st.write(f"Portion: **{grams:.1f} g**")
            st.write(f"Calories: **{nutrition['calories']:.1f} kcal**")
            st.write(f"Carbs: **{nutrition['carbs']:.1f} g**")
            st.write(f"Protein: **{nutrition['protein']:.1f} g**")
            st.write(f"Fat: **{nutrition['fat']:.1f} g**")
            st.markdown("---")

            total_cal += nutrition["calories"]
            total_carbs += nutrition["carbs"]
            total_protein += nutrition["protein"]
            total_fat += nutrition["fat"]

    st.image(annotated_img, caption="Detected Foods")

    st.header(" Meal Summary")
    st.write(f" Total Calories: **{total_cal:.1f} kcal**")
    st.write(f" Carbs: **{total_carbs:.1f} g**")
    st.write(f" Protein: **{total_protein:.1f} g**")
    st.write(f" Fat: **{total_fat:.1f} g**")

    st.header(" Personalized Feedback")
    bmi = weight / ((height/100)**2)
    st.write(f"BMI: **{bmi:.2f}**")
    st.write(f"Daily Calorie Need: **{daily_calories:.0f} kcal**")

    if goal == "weight_loss" and total_cal > daily_calories * 0.35:
        st.warning(" High calorie meal for weight loss")
    if diabetes and total_carbs > 30:
        st.warning(" High carbs for diabetes")
    if total_fat > 40:
        st.warning(" High fat meal")
    if total_protein > 35:
        st.success(" Protein rich meal!")
