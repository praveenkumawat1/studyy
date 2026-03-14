"""
Enhanced Model Training Module
Includes:
- Cross-validation
- Overfitting/Underfitting detection
- Model comparison
- Hyperparameter tuning
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import matplotlib.pyplot as plt
from preprocess_data import DataPreprocessor
import warnings

warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.models = {}
        self.cv_results = {}
        self.best_model = None
        
    def train_random_forest(self):
        """Train RandomForest model"""
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['RandomForest'] = model
        return model
    
    def train_gradient_boosting(self):
        """Train Gradient Boosting model"""
        model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            random_state=42
        )
        model.fit(self.X_train, self.y_train)
        self.models['GradientBoosting'] = model
        return model
    
    def train_ridge_regression(self):
        """Train Ridge Regression model"""
        model = Ridge(alpha=1.0)
        model.fit(self.X_train, self.y_train)
        self.models['Ridge'] = model
        return model
    
    def cross_validation(self, k_folds=5):
        """Perform k-fold cross-validation for all models"""
        print(f"\n{'='*60}")
        print(f"CROSS-VALIDATION RESULTS (k={k_folds})")
        print(f"{'='*60}")
        
        kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
        
        for name, model in self.models.items():
            # Multiple metrics for cross-validation
            scoring = ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error']
            cv_results = cross_validate(model, self.X_train, self.y_train, 
                                       cv=kf, scoring=scoring, return_train_score=True)
            
            self.cv_results[name] = cv_results
            
            print(f"\n{name}:")
            print(f"  CV R² Score: {cv_results['test_r2'].mean():.4f} (+/- {cv_results['test_r2'].std():.4f})")
            print(f"  CV MAE: {-cv_results['test_neg_mean_absolute_error'].mean():.4f} (+/- {cv_results['test_neg_mean_absolute_error'].std():.4f})")
            
    def check_overfitting(self):
        """Check for overfitting/underfitting"""
        print(f"\n{'='*60}")
        print(f"OVERFITTING/UNDERFITTING ANALYSIS")
        print(f"{'='*60}")
        
        for name, model in self.models.items():
            # Training score
            train_pred = model.predict(self.X_train)
            train_r2 = r2_score(self.y_train, train_pred)
            train_mae = mean_absolute_error(self.y_train, train_pred)
            
            # Test score
            test_pred = model.predict(self.X_test)
            test_r2 = r2_score(self.y_test, test_pred)
            test_mae = mean_absolute_error(self.y_test, test_pred)
            
            # Gap analysis
            r2_gap = train_r2 - test_r2
            mae_gap = train_mae - test_mae
            
            print(f"\n{name}:")
            print(f"  Training R²: {train_r2:.4f}")
            print(f"  Testing R²:  {test_r2:.4f}")
            print(f"  R² Gap: {r2_gap:.4f}", end="")
            
            if r2_gap > 0.15:
                print(" ⚠️ OVERFITTING DETECTED")
            elif r2_gap < -0.05:
                print(" ⚠️ UNDERFITTING DETECTED")
            else:
                print(" ✓ GOOD FIT")
            
            print(f"\n  Training MAE: {train_mae:.4f}")
            print(f"  Testing MAE:  {test_mae:.4f}")
            print(f"  MAE Gap: {mae_gap:.4f}")
            
            # Classification
            if r2_gap > 0.15 or test_r2 < train_r2 * 0.90:
                status = "OVERFITTING"
            elif test_r2 < 0.6 and train_r2 < 0.65:
                status = "UNDERFITTING"
            else:
                status = "BALANCED"
            
            print(f"  Status: {status}")
    
    def evaluate_models(self):
        """Comprehensive model evaluation on test set"""
        print(f"\n{'='*60}")
        print(f"TEST SET PERFORMANCE EVALUATION")
        print(f"{'='*60}\n")
        
        results = {}
        for name, model in self.models.items():
            predictions = model.predict(self.X_test)
            
            r2 = r2_score(self.y_test, predictions)
            mae = mean_absolute_error(self.y_test, predictions)
            rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
            
            results[name] = {'R2': r2, 'MAE': mae, 'RMSE': rmse}
            
            print(f"{name}:")
            print(f"  R² Score: {r2:.4f}")
            print(f"  MAE: {mae:.4f}")
            print(f"  RMSE: {rmse:.4f}\n")
        
        # Select best model
        best_name = max(results, key=lambda x: results[x]['R2'])
        self.best_model = self.models[best_name]
        
        print(f"{'='*60}")
        print(f"BEST MODEL: {best_name}")
        print(f"{'='*60}")
        
        return self.best_model, best_name
    
    def train_all(self):
        """Train all models"""
        print("Training RandomForest...")
        self.train_random_forest()
        
        print("Training GradientBoosting...")
        self.train_gradient_boosting()
        
        print("Training Ridge Regression...")
        self.train_ridge_regression()
        
        print("✓ All models trained!")
    
    def save_best_model(self, filename='best_student_model.pkl'):
        """Save the best model"""
        if self.best_model is not None:
            joblib.dump(self.best_model, filename)
            print(f"\n✓ Model saved as '{filename}'")
            return filename
        else:
            print("No best model selected. Run evaluate_models() first.")
            return None

def main():
    # Preprocessing
    print("="*60)
    print("PREPROCESSING DATA")
    print("="*60)
    
    preprocessor = DataPreprocessor("student_data.csv")
    X_train, X_test, y_train, y_test = preprocessor.get_preprocessed_data()
    
    # Training
    print("\n" + "="*60)
    print("MODEL TRAINING")
    print("="*60)
    
    trainer = ModelTrainer(X_train, X_test, y_train, y_test)
    trainer.train_all()
    
    # Evaluation
    trainer.cross_validation(k_folds=5)
    trainer.check_overfitting()
    trainer.evaluate_models()
    
    # Save best model
    trainer.save_best_model('best_student_model.pkl')
    
    print("\n" + "="*60)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    main()
