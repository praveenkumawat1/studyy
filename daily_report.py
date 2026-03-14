import pandas as pd
from datetime import datetime

# load study sessions
df = pd.read_csv("study_sessions.csv")

# today's date
today = datetime.now().strftime("%Y-%m-%d")

today_data = df[df["date"] == today]

print("\n===== DAILY STUDY REPORT =====\n")

if today_data.empty:
    print("No study sessions recorded today.")
else:

    total_hours = today_data["study_hours"].sum()
    subjects = today_data["course_name"].unique()

    print("Date:", today)
    print("Subjects studied:", ", ".join(subjects))
    print("Total study hours today:", total_hours)

    # productivity classification
    if total_hours >= 6:
        status = "Highly Productive"
    elif total_hours >= 3:
        status = "Productive"
    else:
        status = "Needs Improvement"

    print("Daily Status:", status)

print("\n==============================\n")