import pandas as pd

# load study sessions
df = pd.read_csv("study_sessions.csv")

# total hours per subject
subject_hours = df.groupby("course_name")["study_hours"].sum()

# find weak subjects (less study time)
weak_subjects = subject_hours.sort_values()

print("\nSubject Performance:")
print(subject_hours)

print("\nWeak Subjects (Need More Focus):")
print(weak_subjects.head(2))

# generate timetable
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

subjects = list(subject_hours.index)

schedule = {}

for i, day in enumerate(days):

    subject = subjects[i % len(subjects)]

    schedule[day] = subject

print("\nRecommended Study Timetable for Next Week:\n")

for day, subject in schedule.items():
    print(day, "→", subject)