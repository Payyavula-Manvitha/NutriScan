import pandas as pd
import os
from datetime import datetime

FILE = "meal_history.csv"


def save_meal(calories, carbs, protein, fat):

    date = datetime.now().date()

    data = {
        "Date": [date],
        "Calories": [calories],
        "Carbs": [carbs],
        "Protein": [protein],
        "Fat": [fat]
    }

    df = pd.DataFrame(data)

    if os.path.exists(FILE):
        df.to_csv(FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(FILE, index=False)


def load_history():

    if os.path.exists(FILE):
        return pd.read_csv(FILE)

    return None