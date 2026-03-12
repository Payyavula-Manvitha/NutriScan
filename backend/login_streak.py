import pandas as pd
import os
from datetime import datetime, timedelta

FILE = "login_history.csv"


def save_login():

    today = datetime.now().date()

    data = {"Date":[today]}

    df = pd.DataFrame(data)

    if os.path.exists(FILE):

        old = pd.read_csv(FILE)

        if str(today) not in old["Date"].astype(str).values:
            df.to_csv(FILE,mode="a",header=False,index=False)

    else:
        df.to_csv(FILE,index=False)



def calculate_streak():

    if not os.path.exists(FILE):
        return 0,0,0

    history = pd.read_csv(FILE)

    history["Date"] = pd.to_datetime(history["Date"]).dt.date

    dates = sorted(history["Date"].unique())

    today = datetime.now().date()


    # CURRENT STREAK
    current = 0

    for i in range(len(dates)):

        expected = today - timedelta(days=i)

        if expected in dates:
            current += 1
        else:
            break


    # LONGEST STREAK
    longest = 1
    temp = 1

    for i in range(1,len(dates)):

        if dates[i] == dates[i-1] + timedelta(days=1):

            temp += 1

            longest = max(longest,temp)

        else:

            temp = 1


    # DAYS THIS MONTH
    month_days = 0

    for d in dates:

        if d.month == today.month and d.year == today.year:

            month_days += 1


    return current,longest,month_days