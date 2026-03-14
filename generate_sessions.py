import pandas as pd
import random
from datetime import datetime, timedelta

subjects = ["DSA", "Machine Learning", "Operating Systems", "DBMS", "Computer Networks"]

data = []

start_date = datetime(2026,3,1)

for i in range(30):

    date = start_date + timedelta(days=i)

    subjects_today = random.sample(subjects, random.randint(1,3))

    for subject in subjects_today:

        hours = round(random.uniform(0.5,3),1)

        data.append([
            1,
            subject,
            hours,
            date.strftime("%Y-%m-%d")
        ])

df = pd.DataFrame(data, columns=[
    "user_id",
    "course_name",
    "study_hours",
    "date"
])

df.to_csv("study_sessions.csv", index=False)

print("Study sessions dataset generated!")