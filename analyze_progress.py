import pandas as pd
from datetime import datetime, timedelta
import joblib

# load study sessions
df = pd.read_csv("study_sessions.csv")

# convert date
df["date"] = pd.to_datetime(df["date"])

# last 7 days
today = datetime.now()
week_start = today - timedelta(days=7)

weekly_data = df[df["date"] >= week_start]

print("\n===== WEEKLY STUDY REPORT =====\n")

if weekly_data.empty:
    print("No study sessions recorded this week.")
    exit()

# ---------------- WEEKLY CALCULATIONS ----------------

total_hours = weekly_data["study_hours"].sum()

subjects_covered = weekly_data["course_name"].nunique()

study_days = weekly_data["date"].nunique()

idle_days = 7 - study_days

subjects_remaining = max(0, 6 - subjects_covered)

avg_hours = total_hours / study_days

# ---------------- SUBJECT PERFORMANCE ----------------

subject_hours = weekly_data.groupby("course_name")["study_hours"].sum()

percentage = (subject_hours / total_hours) * 100

print("Total Study Hours This Week:", round(total_hours,2))

print("\nSubject Performance (%)")

for subject, value in percentage.items():
    print(subject, ":", round(value,2), "%")

# ---------------- WEAK SUBJECTS ----------------

weak_subjects = percentage.sort_values().head(2)

print("\nSubjects to Focus More On:")

for subject in weak_subjects.index:
    print(subject)

# ---------------- ML PREDICTION ----------------

model = joblib.load("exam_readiness_model.pkl")

data = pd.DataFrame({
    "total_hours":[total_hours],
    "subjects_covered":[subjects_covered],
    "subjects_remaining":[subjects_remaining],
    "study_days":[study_days],
    "idle_days":[idle_days],
    "avg_hours":[avg_hours]
})

prediction = model.predict(data)

score = round(float(prediction[0]),2)

print("\nPredicted Exam Readiness:", score,"%")

if score >= 75:
    status = "Highly Productive"
elif score >= 50:
    status = "Moderately Productive"
else:
    status = "Needs Improvement"

print("Weekly Status:", status)

print("\n===============================\n")