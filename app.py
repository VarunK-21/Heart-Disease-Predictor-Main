import os
import sys
import pandas as pd
from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundles.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Create Flask app with explicit template/static folders so PyInstaller can find them
template_dir = resource_path("templates")
static_dir = resource_path("static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Load the trained models using resource_path
lr_model = pickle.load(open(resource_path('backend/models/logistic_model.pkl'), 'rb'))
rf_model = pickle.load(open(resource_path('backend/models/random_forest.pkl'), 'rb'))
svm_model = pickle.load(open(resource_path('backend/models/svm_model.pkl'), 'rb'))

# Load the scaler
scaler = pickle.load(open(resource_path('backend/models/scaler.pkl'), 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the POST request
        data = request.get_json()

        # Validate input data
        if not data or 'features' not in data:
            raise ValueError("Invalid input: 'features' key is missing in the request data.")

        # Check if the number of features is correct
        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                         'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
                         'ca', 'thal']

        if len(data['features']) != len(feature_names):
            raise ValueError(f"Invalid input: Expected {len(feature_names)} features, but got {len(data['features'])}.")

        # Convert the input data to a pandas DataFrame
        input_data = pd.DataFrame([data['features']], columns=feature_names)

        # Scale the input data using the scaler
        scaled_input = scaler.transform(input_data)

        # Make predictions with reversed logic (0 = Heart Disease, 1 = Healthy)
        lr_pred = 1 - int(lr_model.predict(scaled_input)[0])
        rf_pred = 1 - int(rf_model.predict(scaled_input)[0])
        svm_pred = 1 - int(svm_model.predict(scaled_input)[0])

        # Get the original probabilities (of heart disease) and reverse them
        lr_prob = (1 - lr_model.predict_proba(scaled_input)[0][1]) * 100
        rf_prob = (1 - rf_model.predict_proba(scaled_input)[0][1]) * 100
        svm_prob = (1 - svm_model.predict_proba(scaled_input)[0][1]) * 100

        # Prepare response
        result = {
            'lr_pred': lr_pred,  # 1 = Healthy, 0 = Heart Disease
            'rf_pred': rf_pred,
            'svm_pred': svm_pred,
            'lr_prob': round(lr_prob, 2),  # Chance of being healthy
            'rf_prob': round(rf_prob, 2),
            'svm_prob': round(svm_prob, 2)
        }

        return jsonify(result)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # For local development keep debug=True; for the final exe we will run via run_gui.py
    app.run(debug=True)
