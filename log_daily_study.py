import pandas as pd
from datetime import datetime

file = "study_sessions.csv"

print("\nEnter today's study details\n")

date = datetime.now().strftime("%Y-%m-%d")

data = []

while True:

    subject = input("Enter Subject Name: ")
    hours = float(input("Hours studied for this subject: "))

    data.append({
        "user_id": 1,
        "course_name": subject,
        "study_hours": hours,
        "date": date
    })

    more = input("Add another subject? (y/n): ")

    if more.lower() not in ["y", "yes"]:
        break

new_rows = pd.DataFrame(data)

# save data
try:
    df = pd.read_csv(file)
    df = pd.concat([df, new_rows], ignore_index=True)
except FileNotFoundError:
    df = new_rows

df.to_csv(file, index=False)

print("\nAll study sessions recorded successfully!")

# ---------------- DAILY REPORT ----------------

today_data = df[df["date"] == date]

total_hours = today_data["study_hours"].sum()

subjects = today_data["course_name"].unique()

print("\n===== DAILY STUDY REPORT =====")

print("Date:", date)
print("Subjects studied:", ", ".join(subjects))
print("Total study hours today:", total_hours)

# productivity logic
if total_hours >= 6:
    status = "Highly Productive"
elif total_hours >= 3:
    status = "Productive"
else:
    status = "Needs Improvement"

print("Daily Status:", status)

print("==============================\n")