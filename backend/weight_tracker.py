import pandas as pd
import os
from datetime import datetime

FILE_PATH = "weight_history.csv"

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
