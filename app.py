from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# load trained model
model = joblib.load("exam_readiness_model.pkl")


@app.get("/")
def home():
    return {"message": "Study Habit Analyzer API Running"}


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame({
        "total_hours":[data["total_hours"]],
        "subjects_covered":[data["subjects_covered"]],
        "subjects_remaining":[data["subjects_remaining"]],
        "study_days":[data["study_days"]],
        "idle_days":[data["idle_days"]],
        "avg_hours":[data["avg_hours"]]
    })

    prediction = model.predict(df)

    score = round(float(prediction[0]),2)

    if score >= 75:
        status = "Highly Productive"
    elif score >= 50:
        status = "Moderately Productive"
    else:
        status = "Needs Improvement"

    return {
        "exam_readiness_score": score,
        "status": status
    }