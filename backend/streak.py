import pandas as pd
from datetime import datetime, timedelta
from history import load_history


def calculate_streak():

    history = load_history()

    # If no history
    if history is None or len(history) == 0:
        return 0

    # If Date column not present, avoid crash
    if "Date" not in history.columns:
        return 0

    history["Date"] = pd.to_datetime(history["Date"]).dt.date

    unique_days = sorted(history["Date"].unique(), reverse=True)

    today = datetime.now().date()

    streak = 0

    for i, day in enumerate(unique_days):

        expected_day = today - timedelta(days=i)

        if day == expected_day:
            streak += 1
        else:
            break

    return streak