import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# Load data
df = pd.read_csv('daily_study_log_sample.csv')

# Features: hours_studied, subject (encoded), notes_length
df['notes_length'] = df['notes'].str.len().fillna(0)
df['weekday'] = pd.to_datetime(df['date']).dt.weekday

le = LabelEncoder()
df['subject_encoded'] = le.fit_transform(df['subject'])

X = df[['hours_studied', 'notes_length', 'weekday', 'subject_encoded']]
y = df['productivity_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)
print('R2:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

joblib.dump(model, 'productivity_model.pkl')
joblib.dump(scaler, 'productivity_scaler.pkl')
joblib.dump(le, 'subject_le.pkl')

print('Productivity model trained!')

