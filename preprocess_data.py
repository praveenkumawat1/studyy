"""
Data Preprocessing Module for Study Tracker
Handles:
- Data cleaning
- Feature engineering
- Feature selection
- Train-test split
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.selected_features = None
        
    def load_data(self):
        """Load the dataset"""
        self.data = pd.read_csv(self.csv_path)
        print(f"Data loaded: {self.data.shape}")
        return self.data
    
    def basic_cleaning(self):
        """Remove missing values and duplicates"""
        initial_shape = self.data.shape
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        # Handle missing values
        self.data = self.data.dropna()
        
        print(f"Data shape after cleaning: {self.data.shape} (removed {initial_shape[0] - self.data.shape[0]} rows)")
        return self.data
    
    def encode_categorical(self):
        """Encode categorical variables"""
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            le = LabelEncoder()
            self.data[col] = le.fit_transform(self.data[col])
            self.label_encoders[col] = le
        
        print(f"Encoded {len(categorical_cols)} categorical columns")
        return self.data
    
    def feature_engineering(self):
        """Create additional features"""
        # Study effectiveness score (combination of studytime, health, and grades)
        self.data['study_effectiveness'] = (
            self.data['studytime'] * 0.3 + 
            self.data['health'] * 0.2 + 
            (self.data['G1'] / 20) * 20 * 0.5
        )
        
        # Academic risk score (inverse - higher is better)
        self.data['academic_risk'] = (
            self.data['failures'] * 2 + 
            self.data['absences'] * 0.5
        )
        
        # Social activity index
        self.data['social_activity'] = (
            self.data['freetime'] + 
            self.data['goout']
        ) / 2
        
        # Previous performance average
        self.data['prev_avg_grade'] = (
            self.data['G1'] + 
            self.data['G2']
        ) / 2
        
        print("Feature engineering completed")
        return self.data
    
    def feature_selection(self, k_features=10):
        """Select most important features using SelectKBest"""
        X = self.data.drop('G3', axis=1)  # target is G3
        y = self.data['G3']
        
        selector = SelectKBest(f_regression, k=min(k_features, X.shape[1]))
        selector.fit(X, y)
        
        # Get selected features
        selected_indices = selector.get_support(indices=True)
        self.selected_features = X.columns[selected_indices].tolist()
        
        print(f"Selected {len(self.selected_features)} features:")
        for feature in self.selected_features:
            print(f"  - {feature}")
        
        return self.selected_features
    
    def prepare_data(self, test_size=0.2, random_state=42):
        """Prepare X and y for modeling"""
        if self.selected_features is None:
            self.feature_selection()
        
        X = self.data[self.selected_features]
        y = self.data['G3']
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        # Convert back to DataFrame
        self.X_train = pd.DataFrame(self.X_train, columns=self.selected_features)
        self.X_test = pd.DataFrame(self.X_test, columns=self.selected_features)
        
        print(f"\nTrain-Test Split:")
        print(f"  Training set: {self.X_train.shape}")
        print(f"  Test set: {self.X_test.shape}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_preprocessed_data(self):
        """Full preprocessing pipeline"""
        self.load_data()
        self.basic_cleaning()
        self.encode_categorical()
        self.feature_engineering()
        self.feature_selection()
        self.prepare_data()
        
        return self.X_train, self.X_test, self.y_train, self.y_test

# Usage
if __name__ == "__main__":
    preprocessor = DataPreprocessor("student_data.csv")
    X_train, X_test, y_train, y_test = preprocessor.get_preprocessed_data()
    
    print("\n✓ Preprocessing completed successfully!")
    print(f"Features used: {preprocessor.selected_features}")
