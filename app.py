import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model and scaler
MODEL_PATH = 'models/loan_xgb_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Numerical features that need scaling
NUM_FEATURES = ['age', 'annual_income', 'credit_score', 'loan_amount',
                'debt_to_income', 'years_employed', 'credit_history_years',
                'total_debt', 'emi', 'interest_rate']

# All features in the exact order required by the model
FEATURE_COLUMNS = [
    'age', 'gender', 'dependents', 'years_employed', 'annual_income',
    'credit_score', 'existing_loans', 'credit_history_years', 'loan_amount',
    'loan_term', 'interest_rate', 'has_cosigner', 'debt_to_income',
    'total_debt', 'emi', 'marital_status_Married', 'marital_status_Single',
    'education_High School', 'education_Master', 'education_PhD',
    'employment_status_Salaried', 'employment_status_Self-Employed',
    'employment_status_Unemployed', 'property_area_Semiurban',
    'property_area_Urban', 'loan_purpose_Business', 'loan_purpose_Education',
    'loan_purpose_Home', 'loan_purpose_Medical', 'loan_purpose_Personal'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Initialize dictionary with zeros
        input_data = {col: 0 for col in FEATURE_COLUMNS}
        
        # 1. Direct assignments
        input_data['age'] = float(data.get('age', 0))
        input_data['dependents'] = float(data.get('dependents', 0))
        input_data['years_employed'] = float(data.get('years_employed', 0))
        input_data['annual_income'] = float(data.get('annual_income', 0))
        input_data['credit_score'] = float(data.get('credit_score', 0))
        input_data['existing_loans'] = float(data.get('existing_loans', 0))
        input_data['credit_history_years'] = float(data.get('credit_history_years', 0))
        input_data['loan_amount'] = float(data.get('loan_amount', 0))
        input_data['loan_term'] = float(data.get('loan_term', 0))
        input_data['interest_rate'] = float(data.get('interest_rate', 0))
        input_data['total_debt'] = float(data.get('total_debt', 0))
        input_data['emi'] = float(data.get('emi', 0))
        input_data['debt_to_income'] = float(data.get('debt_to_income', 0))
        
        # 2. Binary Encoding
        input_data['gender'] = 1 if data.get('gender') == 'Male' else 0
        input_data['has_cosigner'] = 1 if data.get('has_cosigner') == 'Yes' else 0
        
        # 3. Categorical (Dummies - drop_first=True)
        # marital_status: Divorced (baseline), Married, Single
        ms = data.get('marital_status')
        if ms == 'Married': input_data['marital_status_Married'] = 1
        elif ms == 'Single': input_data['marital_status_Single'] = 1
        
        # education: Bachelor (baseline), High School, Master, PhD
        edu = data.get('education')
        if edu == 'High School': input_data['education_High School'] = 1
        elif edu == 'Master': input_data['education_Master'] = 1
        elif edu == 'PhD': input_data['education_PhD'] = 1
        
        # employment_status: Business (baseline), Salaried, Self-Employed, Unemployed
        emp = data.get('employment_status')
        if emp == 'Salaried': input_data['employment_status_Salaried'] = 1
        elif emp == 'Self-Employed': input_data['employment_status_Self-Employed'] = 1
        elif emp == 'Unemployed': input_data['employment_status_Unemployed'] = 1
        
        # property_area: Rural (baseline), Semiurban, Urban
        pa = data.get('property_area')
        if pa == 'Semiurban': input_data['property_area_Semiurban'] = 1
        elif pa == 'Urban': input_data['property_area_Urban'] = 1
        
        # loan_purpose: Auto (baseline), Business, Education, Home, Medical, Personal
        lp = data.get('loan_purpose')
        if lp == 'Business': input_data['loan_purpose_Business'] = 1
        elif lp == 'Education': input_data['loan_purpose_Education'] = 1
        elif lp == 'Home': input_data['loan_purpose_Home'] = 1
        elif lp == 'Medical': input_data['loan_purpose_Medical'] = 1
        elif lp == 'Personal': input_data['loan_purpose_Personal'] = 1
        
        # Convert to DataFrame
        X = pd.DataFrame([input_data])[FEATURE_COLUMNS]
        
        # 4. Scaling
        X[NUM_FEATURES] = scaler.transform(X[NUM_FEATURES])
        
        # 5. Prediction
        prediction = int(model.predict(X)[0])
        probability = float(model.predict_proba(X)[0][1])
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'status': 'Approved' if prediction == 1 else 'Rejected',
            'probability': probability,
            'message': 'Confidence: {:.1f}%'.format(probability * 100 if prediction == 1 else (1-probability) * 100)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
