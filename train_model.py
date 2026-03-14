import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# ---------------- LOAD DATA ----------------

data = pd.read_csv("student_data.csv")

# ---------------- PREPROCESSING ----------------

# convert categorical columns
label = LabelEncoder()

categorical_cols = data.select_dtypes(include=['object']).columns

for col in categorical_cols:
    data[col] = label.fit_transform(data[col])

# ---------------- FEATURES ----------------

X = data.drop("G3", axis=1)  # final grade
y = data["G3"]

# ---------------- TRAIN TEST SPLIT ----------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------

y_pred = model.predict(X_test)

print("R2 Score:", r2_score(y_test, y_pred))
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))

# ---------------- SAVE MODEL ----------------

joblib.dump(model, "student_performance_model.pkl")

print("\nModel trained and saved successfully!")