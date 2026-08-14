# CreditWise: Advanced Loan Classification System

CreditWise is a production-ready machine learning application designed to predict loan eligibility for applicants based on a comprehensive set of financial and personal parameters. Built with **XGBoost** and **Flask**, the system achieves high accuracy and provides an intuitive, high-performance web interface.

## 🚀 Key Features

- **High-Precision ML Model**: Utilizes a tuned XGBoost classifier trained on 5,000+ loan applications.
- **Real-time Prediction**: Deep analysis of 30+ features, including credit score, DTI ratio, and employment history.
- **Modern Web Interface**: A premium, responsive UI built with Glassmorphism aesthetics and micro-animations.
- **Modular Pipeline**: Full research-to-production pipeline included (EDA, Preprocessing, Hyperparameter Tuning).

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Scikit-learn, XGBoost, Joblib
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript (ES6+)
- **Data Science**: Pandas, NumPy, Seaborn, Matplotlib

## 📂 Project Structure

```
loan_classification/
├── app.py                # Production Flask API
├── Loan_Classification.py # Research & Model Training Pipeline
├── requirements.txt       # System Dependencies
├── models/                # Serialized Model & Scaler
│   ├── loan_xgb_model.pkl
│   └── scaler.pkl
├── static/                # Frontend Assets (CSS/JS)
│   ├── css/style.css
│   └── js/script.js
├── templates/             # HTML Templates
│   └── index.html
├── data/                  # Raw Dataset
│   └── loan_detection.csv
└── outputs/               # Visualizations & Training Reports
    ├── figures/
    └── reports/
```

## 📖 Model Insights

The final model focuses on several critical features:
1. **Debt-to-Income Ratio**: The most significant predictor of approval status.
2. **Credit History**: Years of credit history and credit score provide a reliable risk profile.
3. **Employment Stability**: Years employed and current employment status are key filters.

## 🏁 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train Model (Optional)**:
   ```bash
   python Loan_Classification.py
   ```

3. **Launch Application**:
   ```bash
   python app.py
   ```
   Access the system at `http://localhost:5001`.

## 📈 Performance Summary

- **Accuracy**: 91.3%
- **F1-Score**: 0.92
- **ROC-AUC**: 0.98

---
*Created for Submission - CreditWise Financial System*
