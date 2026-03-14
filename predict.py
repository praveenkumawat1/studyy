import joblib
import pandas as pd

model = joblib.load("student_performance_model.pkl")

print("\nEnter Student Study Details\n")

studytime = int(input("Study Time (1-4): "))
failures = int(input("Past Failures: "))
absences = int(input("Absences: "))
freetime = int(input("Free Time (1-5): "))
goout = int(input("Going Out Frequency (1-5): "))
health = int(input("Health (1-5): "))
G1 = int(input("First Period Grade: "))
G2 = int(input("Second Period Grade: "))

data = pd.DataFrame({
    "studytime":[studytime],
    "failures":[failures],
    "absences":[absences],
    "freetime":[freetime],
    "goout":[goout],
    "health":[health],
    "G1":[G1],
    "G2":[G2]
})

prediction = model.predict(data)

score = round(prediction[0],2)

print("\nPredicted Final Grade:", score)

if score >= 15:
    print("Status: Excellent Performance")
elif score >= 10:
    print("Status: Average Performance")
else:
    print("Status: Needs Improvement")