import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import joblib
import random

# Create dataset
data = []
for i in range(5000):
    total_hours = random.uniform(5, 40)
    subjects_covered = random.randint(1, 8)
    study_days = random.randint(3, 7)
    avg_prod = random.uniform(2, 4.5)
    consistency = study_days / 7.0
    readiness = min(100, max(0, int(total_hours * 1.5 + avg_prod * 20 + consistency * 30 + subjects_covered * 5)))
    data.append([total_hours, subjects_covered, study_days, avg_prod, consistency, readiness])
df = pd.DataFrame(data, columns=['total_hours', 'subjects_covered', 'study_days', 'avg_prod', 'consistency', 'readiness'])
df.to_csv('study_dataset.csv', index=False)
print('Dataset created:', df.shape)

X = df[['total_hours', 'subjects_covered', 'study_days', 'avg_prod', 'consistency']]
y = df['readiness']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print('R2:', r2_score(y_test, y_pred))
from sklearn.metrics import mean_absolute_error
print('MAE:', mean_absolute_error(y_test, y_pred))

joblib.dump(model, 'exam_readiness_model.pkl')
joblib.dump(scaler, 'exam_readiness_scaler.pkl')

print('Exam readiness model trained and saved!')
