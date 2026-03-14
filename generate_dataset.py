import pandas as pd
import random

data = []

for i in range(2000):

    total_hours = random.randint(2, 40)

    subjects_covered = random.randint(1, 6)

    subjects_remaining = 6 - subjects_covered

    study_days = random.randint(1, 7)

    idle_days = 7 - study_days

    avg_hours = round(total_hours / study_days, 2)

    readiness = min(100, int(
        (total_hours * 1.5) +
        (subjects_covered * 8) +
        (study_days * 5) -
        (idle_days * 4)
    ))

    readiness = max(0, readiness)

    data.append([
        total_hours,
        subjects_covered,
        subjects_remaining,
        study_days,
        idle_days,
        avg_hours,
        readiness
    ])

columns = [
    "total_hours",
    "subjects_covered",
    "subjects_remaining",
    "study_days",
    "idle_days",
    "avg_hours",
    "exam_readiness"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("study_dataset.csv", index=False)

print("Dataset generated successfully!")