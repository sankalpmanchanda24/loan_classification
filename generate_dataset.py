# =============================================================
# SYNTHETIC LOAN DETECTION DATASET GENERATOR
# Brainstormed features based on real-world loan approval patterns
# =============================================================
import numpy as np
import pandas as pd

np.random.seed(42)
N = 5000

# ---------- Demographics ----------
age = np.clip(np.random.normal(38, 12, N).astype(int), 21, 70)
gender = np.random.choice(['Male', 'Female'], N, p=[0.62, 0.38])
marital_status = np.random.choice(
    ['Single', 'Married', 'Divorced'], N, p=[0.35, 0.55, 0.10])
education = np.random.choice(
    ['High School', 'Bachelor', 'Master', 'PhD'], N, p=[0.40, 0.35, 0.18, 0.07])
dependents = np.random.choice([0, 1, 2, 3, 4], N, p=[0.35, 0.30, 0.20, 0.10, 0.05])

# ---------- Employment ----------
employment_status = np.random.choice(
    ['Salaried', 'Self-Employed', 'Business', 'Unemployed'],
    N, p=[0.55, 0.20, 0.15, 0.10])
years_employed = np.clip(
    np.where(employment_status == 'Unemployed', 0,
             np.random.normal(8, 6, N)), 0, 40).astype(int)

# Income depends on education & employment
edu_mult = {'High School': 0.7, 'Bachelor': 1.0, 'Master': 1.3, 'PhD': 1.6}
emp_mult = {'Salaried': 1.0, 'Self-Employed': 1.2, 'Business': 1.5, 'Unemployed': 0.0}
base_income = np.random.normal(60000, 25000, N)
annual_income = base_income * \
    np.array([edu_mult[e] for e in education]) * \
    np.array([emp_mult[e] for e in employment_status])
annual_income = np.clip(annual_income, 15000, 250000).astype(int)

# ---------- Credit ----------
credit_score = np.clip(np.random.normal(680, 80, N).astype(int), 300, 850)
existing_loans = np.random.choice([0, 1, 2, 3, 4], N, p=[0.45, 0.30, 0.15, 0.07, 0.03])
credit_history_years = np.clip(np.random.normal(8, 5, N), 0, 30).astype(int)

# ---------- Loan Request ----------
loan_amount = np.clip(np.random.normal(150000, 80000, N), 5000, 500000).astype(int)
loan_term = np.random.choice([12, 24, 36, 60, 120, 240], N, p=[0.10, 0.15, 0.25, 0.30, 0.15, 0.05])
loan_purpose = np.random.choice(
    ['Home', 'Auto', 'Education', 'Business', 'Medical', 'Personal'],
    N, p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10])
interest_rate = np.clip(5 + (850 - credit_score) / 50 +
                        np.random.normal(0, 1, N), 3, 25).round(2)
property_area = np.random.choice(
    ['Urban', 'Semiurban', 'Rural'], N, p=[0.45, 0.35, 0.20])
has_cosigner = np.random.choice(['Yes', 'No'], N, p=[0.25, 0.75])

# ---------- Derived Features ----------
debt_to_income = ((loan_amount / loan_term) * 12) / annual_income
debt_to_income = np.round(debt_to_income, 3)
total_debt = existing_loans * 25000 + loan_amount
emi = loan_amount / loan_term

# ---------- Target Variable (Loan Status) ----------
# Logistic function based on key features
logit = (
    0.00002 * annual_income
    + 0.008 * credit_score
    - 8.0 * debt_to_income
    + 0.15 * years_employed
    + 0.5 * credit_history_years
    - 0.3 * existing_loans
    + 1.5 * (has_cosigner == 'Yes')
    - 2.0 * (employment_status == 'Unemployed')
    + 0.8 * (property_area == 'Urban')
    - 5.5  # intercept
)
prob = 1 / (1 + np.exp(-logit))
loan_status = (np.random.rand(N) < prob).astype(int)

# ---------- Build DataFrame ----------
df = pd.DataFrame({
    'applicant_id': [f'APP{100000+i}' for i in range(N)],
    'age': age,
    'gender': gender,
    'marital_status': marital_status,
    'education': education,
    'dependents': dependents,
    'employment_status': employment_status,
    'years_employed': years_employed,
    'annual_income': annual_income,
    'credit_score': credit_score,
    'existing_loans': existing_loans,
    'credit_history_years': credit_history_years,
    'loan_amount': loan_amount,
    'loan_term': loan_term,
    'loan_purpose': loan_purpose,
    'interest_rate': interest_rate,
    'property_area': property_area,
    'has_cosigner': has_cosigner,
    'debt_to_income': debt_to_income,
    'total_debt': total_debt,
    'emi': np.round(emi, 2),
    'loan_status': loan_status
})

# Save
df.to_csv('data/loan_detection.csv', index=False)
print(f'Generated {df.shape[0]:,} rows × {df.shape[1]} columns')
print(f'Approval rate: {df["loan_status"].mean()*100:.1f}%')
print(f'Saved: data/loan_detection.csv')
print(f'\nFirst 3 rows:')
print(df.head(3))
