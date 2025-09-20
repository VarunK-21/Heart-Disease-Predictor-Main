import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

# Load the trained models and scaler from disk
lr_model = pickle.load(open('backend/models/logistic_model.pkl', 'rb'))
rf_model = pickle.load(open('backend/models/random_forest.pkl', 'rb'))
svm_model = pickle.load(open('backend/models/svm_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))

# Define the feature names based on your dataset
feature_columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 
    'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Example input data for 2-3 healthy individualsp
healthy_person_1 = [65,0,2,155,269,0,1,148,0,0.8,2,0,2]  # Healthy individual example


# Combine these individual data into a list
input_data = np.array([healthy_person_1, ])

# Convert the input data into a DataFrame
input_df = pd.DataFrame(input_data, columns=feature_columns)

# Scale the input data using the same scaler
scaled_input_data = scaler.transform(input_df)

# Get the probabilities for Logistic Regression
lr_prob = lr_model.predict_proba(scaled_input_data)[:, 1] * 100  # Probability of heart disease

# Get the probabilities for Random Forest
rf_prob = rf_model.predict_proba(scaled_input_data)[:, 1] * 100  # Probability of heart disease

# Get the probabilities for SVM
svm_prob = svm_model.predict_proba(scaled_input_data)[:, 1] * 100  # Probability of heart disease

# Print predictions and probabilities
print("Logistic Regression Probability (in %):", lr_prob)
print("Random Forest Probability (in %):", rf_prob)
print("SVM Probability (in %):", svm_prob)
