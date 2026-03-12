from fastapi import FastAPI, File, UploadFile
import shutil, os, cv2

from yolo.model import detect_food
from agents.portion_agent import estimate_portion
from agents.nutrition_agent import estimate_nutrition

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(path)
    h, w, _ = img.shape

    detections = detect_food(path)

    if not detections:
        return {"message": "No food detected"}

    bbox = detections[0]["bbox"]
    size_factor, portion = estimate_portion(bbox, w, h)

    food = "pizza"  # TEMP for mid-review
    nutrition = estimate_nutrition(food, size_factor)

    return {
        "food": food,
        "portion": portion,
        "nutrition": nutrition
    }
