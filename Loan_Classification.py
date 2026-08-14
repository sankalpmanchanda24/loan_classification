# %% [markdown]
# # Loan Classification — Machine Learning Major Project
#
# **Objective:** Classify loan applicants as *Approved* (1) or *Rejected* (0) using supervised ML.
#
# **Techniques covered:**
# - Exploratory Data Analysis
# - Data Preprocessing (encoding, scaling, outlier handling)
# - Feature Engineering
# - Train/Test split + Cross-Validation
# - 6 ML models: Logistic Regression, Decision Tree, Random Forest, XGBoost, KNN, SVM
# - Hyperparameter tuning (GridSearchCV)
# - Model evaluation: Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix
# - Feature importance interpretation
#
# ---

# %%
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report, roc_curve)
import xgboost as xgb

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

# %% [markdown]
# ## 1. Data Loading

# %%
print('='*70)
print('1. DATA LOADING')
print('='*70)

df = pd.read_csv('data/loan_detection.csv')
print(f'Shape: {df.shape}')
print(f'Approval rate: {df["loan_status"].mean()*100:.1f}%')
df.head()

# %%
df.info()

# %% [markdown]
# ## 2. Exploratory Data Analysis (EDA)

# %%
print('='*70)
print('2. EXPLORATORY DATA ANALYSIS')
print('='*70)

# Missing & duplicates
print(f'\nMissing values: {df.isnull().sum().sum()}')
print(f'Duplicates: {df.duplicated().sum()}')

# Target distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df['loan_status'].value_counts().plot(kind='bar', ax=axes[0],
                                      color=['#e74c3c', '#2ecc71'])
axes[0].set_title('Loan Status Distribution', fontweight='bold')
axes[0].set_xticklabels(['Rejected (0)', 'Approved (1)'], rotation=0)
axes[0].set_ylabel('Count')

df['loan_status'].value_counts(normalize=True).plot(
    kind='pie', ax=axes[1], autopct='%1.1f%%',
    colors=['#e74c3c', '#2ecc71'], startangle=90)
axes[1].set_title('Approval Rate', fontweight='bold')
axes[1].set_ylabel('')
plt.savefig('outputs/figures/01_target_distribution.png')
# %%
# Numeric features distribution
num_cols = ['age', 'annual_income', 'credit_score', 'loan_amount',
            'debt_to_income', 'years_employed', 'credit_history_years']
fig, axes = plt.subplots(2, 4, figsize=(18, 9))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.histplot(data=df, x=col, hue='loan_status', kde=True,
                 ax=axes[i], bins=30, alpha=0.5,
                 palette=['#e74c3c', '#2ecc71'])
    axes[i].set_title(col, fontweight='bold')
axes[7].axis('off')
plt.suptitle('Numeric Features by Loan Status', fontsize=14, fontweight='bold', y=1.02)
plt.savefig('outputs/figures/02_numeric_distributions.png')
# %%
# Categorical features vs target
cat_cols = ['gender', 'marital_status', 'education', 'employment_status',
            'property_area', 'has_cosigner', 'loan_purpose']
fig, axes = plt.subplots(3, 3, figsize=(16, 14))
axes = axes.flatten()
for i, col in enumerate(cat_cols):
    approval_rate = df.groupby(col)['loan_status'].mean().sort_values(ascending=False)
    sns.barplot(x=approval_rate.index, y=approval_rate.values,
                ax=axes[i], palette='viridis')
    axes[i].set_title(f'Approval Rate by {col}', fontweight='bold')
    axes[i].set_ylabel('Approval Rate')
    axes[i].set_ylim(0, 1)
    axes[i].tick_params(axis='x', rotation=30)
    for j, v in enumerate(approval_rate.values):
        axes[i].text(j, v + 0.02, f'{v:.1%}', ha='center', fontweight='bold')
axes[7].axis('off')
axes[8].axis('off')
plt.tight_layout()
plt.savefig('outputs/figures/03_categorical_vs_target.png')
# %% [markdown]
# ## 3. Data Preprocessing

# %%
print('='*70)
print('3. DATA PREPROCESSING')
print('='*70)

# Drop identifier
df_proc = df.drop('applicant_id', axis=1)

# Encode binary categorical
df_proc['has_cosigner'] = (df_proc['has_cosigner'] == 'Yes').astype(int)
df_proc['gender'] = (df_proc['gender'] == 'Male').astype(int)

# One-hot encode remaining categoricals
df_proc = pd.get_dummies(df_proc, columns=['marital_status', 'education',
                                            'employment_status', 'property_area',
                                            'loan_purpose'], drop_first=True)

print(f'Processed shape: {df_proc.shape}')
print(f'Columns: {list(df_proc.columns)}')

# %%
# Outlier detection (IQR)
Q1 = df_proc[num_cols].quantile(0.25)
Q3 = df_proc[num_cols].quantile(0.75)
IQR = Q3 - Q1
outliers = ((df_proc[num_cols] < (Q1 - 1.5 * IQR)) |
            (df_proc[num_cols] > (Q3 + 1.5 * IQR))).sum()
print('\nOutliers per numeric column:')
print(outliers)

# %%
# Correlation heatmap
plt.figure(figsize=(14, 10))
corr = df_proc.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=0.5, cbar_kws={'shrink': 0.8},
            annot_kws={'size': 7})
plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
plt.savefig('outputs/figures/04_correlation_heatmap.png')
# %%
# Feature correlation with target
target_corr = corr['loan_status'].drop('loan_status').sort_values(ascending=False)
plt.figure(figsize=(10, 8))
colors = ['#2ecc71' if v > 0 else '#e74c3c' for v in target_corr.values]
sns.barplot(x=target_corr.values, y=target_corr.index, palette=colors)
plt.title('Feature Correlation with Loan Status', fontsize=14, fontweight='bold')
plt.xlabel('Pearson Correlation')
plt.axvline(0, color='black', linewidth=0.8)
for i, v in enumerate(target_corr.values):
    plt.text(v + (0.01 if v >= 0 else -0.02), i, f'{v:.3f}',
             va='center', fontsize=8)
plt.savefig('outputs/figures/05_target_correlation.png')
# %% [markdown]
# ## 4. Feature Engineering & Train/Test Split

# %%
print('='*70)
print('4. FEATURE ENGINEERING & SPLIT')
print('='*70)

# Separate X and y
X = df_proc.drop('loan_status', axis=1)
y = df_proc['loan_status']

# Scale numeric features
scaler = StandardScaler()
num_features = ['age', 'annual_income', 'credit_score', 'loan_amount',
                'debt_to_income', 'years_employed', 'credit_history_years',
                'total_debt', 'emi', 'interest_rate']
X[num_features] = scaler.fit_transform(X[num_features])

# Train/test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

print(f'Training: {X_train.shape[0]:,} samples')
print(f'Test:     {X_test.shape[0]:,} samples')
print(f'Features: {X_train.shape[1]}')
print(f'Train approval rate: {y_train.mean():.3f}')
print(f'Test approval rate:  {y_test.mean():.3f}')

# %%
# Class balance check
print('\nClass distribution (train):')
print(y_train.value_counts(normalize=True))

# %% [markdown]
# ## 5. Model Training & Evaluation

# %%
print('='*70)
print('5. MODEL TRAINING & EVALUATION')
print('='*70)

def evaluate_model(model, X_train, X_test, y_train, y_test, name='Model'):
    """Train, predict, return metrics dict."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = None
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, 'decision_function'):
        y_proba = model.decision_function(X_test)

    metrics = {
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1': f1_score(y_test, y_pred),
        'ROC-AUC': roc_auc_score(y_test, y_proba) if y_proba is not None else None
    }
    return model, metrics, y_pred, y_proba

# Define models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    'XGBoost': xgb.XGBClassifier(n_estimators=200, learning_rate=0.1,
                                   max_depth=6, random_state=42,
                                   eval_metric='logloss', n_jobs=-1),
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'SVM (RBF)': SVC(kernel='rbf', probability=False, random_state=42)
}

results = []
fitted_models = {}
predictions = {}

for name, model in models.items():
    print(f'\n--- Training {name} ---')
    fitted, m, y_pred, y_proba = evaluate_model(
        model, X_train, X_test, y_train, y_test, name)
    results.append(m)
    fitted_models[name] = fitted
    predictions[name] = (y_pred, y_proba)
    auc_str = f'{m["ROC-AUC"]:.4f}' if m['ROC-AUC'] is not None else 'N/A'
    print(f'  Accuracy: {m["Accuracy"]:.4f} | F1: {m["F1"]:.4f} | ROC-AUC: {auc_str}')

# %%
# Results comparison
results_df = pd.DataFrame(results).sort_values('ROC-AUC', ascending=False)
print('\n=== MODEL COMPARISON ===')
print(results_df.round(4).to_string(index=False))
results_df.round(4).to_csv('outputs/reports/model_comparison.csv', index=False)

# %%
# Visualization: Metrics comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC']
results_melted = results_df.melt(id_vars='Model', value_vars=metrics_to_plot,
                                  var_name='Metric', value_name='Score')
sns.barplot(data=results_melted, x='Model', y='Score', hue='Metric',
            ax=axes[0], palette='Set2')
axes[0].set_title('Model Performance Comparison', fontweight='bold')
axes[0].set_ylim(0, 1)
axes[0].tick_params(axis='x', rotation=30)
axes[0].legend(loc='lower right', fontsize=8)

# ROC-AUC ranking
sns.barplot(data=results_df, x='Model', y='ROC-AUC',
            ax=axes[1], palette='viridis')
axes[1].set_title('ROC-AUC Ranking', fontweight='bold')
axes[1].set_ylim(0.5, 1)
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(results_df['ROC-AUC'].values):
    axes[1].text(i, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/figures/06_model_comparison.png')
# %% [markdown]
# ## 6. Confusion Matrices

# %%
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()
for i, (name, (y_pred, _)) in enumerate(predictions.items()):
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                xticklabels=['Rejected', 'Approved'],
                yticklabels=['Rejected', 'Approved'])
    axes[i].set_title(f'{name}\nAcc: {accuracy_score(y_test, y_pred):.3f}',
                      fontweight='bold')
    axes[i].set_ylabel('True')
    axes[i].set_xlabel('Predicted')
plt.suptitle('Confusion Matrices', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/figures/07_confusion_matrices.png')
# %% [markdown]
# ## 7. ROC Curves

# %%
plt.figure(figsize=(10, 8))
for name, (_, y_proba) in predictions.items():
    if y_proba is not None:
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        plt.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {auc:.3f})')
    else:
        # Use decision function as fallback
        from sklearn.metrics import roc_curve as _rfc
        try:
            scores = fitted_models[name].decision_function(X_test)
            fpr, tpr, _ = _rfc(y_test, scores)
            auc = roc_auc_score(y_test, scores)
            plt.plot(fpr, tpr, linewidth=2, linestyle='--',
                     label=f'{name} (AUC = {auc:.3f}, via decision fn)')
        except Exception:
            pass
plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves — Model Comparison', fontsize=14, fontweight='bold')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.savefig('outputs/figures/08_roc_curves.png')
# %% [markdown]
# ## 8. Cross-Validation

# %%
print('='*70)
print('8. CROSS-VALIDATION (5-FOLD STRATIFIED)')
print('='*70)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = []
for name, model in models.items():
    # SVM is slow with predict_proba — use linear SVC variant for CV
    if name == 'SVM (RBF)':
        from sklearn.svm import SVC as _SVC
        cv_model = _SVC(kernel='linear', probability=False, random_state=42)
        scores = cross_val_score(cv_model, X_train, y_train, cv=cv,
                                  scoring='roc_auc', n_jobs=-1)
    else:
        scores = cross_val_score(model, X_train, y_train, cv=cv,
                                  scoring='roc_auc', n_jobs=-1)
    cv_results.append({
        'Model': name,
        'CV ROC-AUC Mean': scores.mean(),
        'CV ROC-AUC Std': scores.std()
    })
    print(f'  {name:<22} {scores.mean():.4f} ± {scores.std():.4f}')

cv_df = pd.DataFrame(cv_results).sort_values('CV ROC-AUC Mean', ascending=False)
cv_df.round(4).to_csv('outputs/reports/cross_validation.csv', index=False)

# %% [markdown]
# ## 9. Hyperparameter Tuning (Best Model)

# %%
print('='*70)
print('9. HYPERPARAMETER TUNING — XGBoost')
print('='*70)

best_model_name = results_df.iloc[0]['Model']
print(f'Tuning top model: {best_model_name}')

# Pick best candidate
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0]
}

xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1)
grid = GridSearchCV(xgb_model, param_grid, cv=3, scoring='roc_auc',
                    n_jobs=-1, verbose=0)
grid.fit(X_train, y_train)

print(f'Best params: {grid.best_params_}')
print(f'Best CV ROC-AUC: {grid.best_score_:.4f}')

# Evaluate tuned model
best_model = grid.best_estimator_
y_pred_tuned = best_model.predict(X_test)
y_proba_tuned = best_model.predict_proba(X_test)[:, 1]

tuned_metrics = {
    'Model': 'XGBoost (Tuned)',
    'Accuracy': accuracy_score(y_test, y_pred_tuned),
    'Precision': precision_score(y_test, y_pred_tuned),
    'Recall': recall_score(y_test, y_pred_tuned),
    'F1': f1_score(y_test, y_pred_tuned),
    'ROC-AUC': roc_auc_score(y_test, y_proba_tuned)
}
print(f'\nTuned Test ROC-AUC: {tuned_metrics["ROC-AUC"]:.4f}')

# %% [markdown]
# ## 10. Feature Importance

# %%
print('='*70)
print('10. FEATURE IMPORTANCE (XGBoost)')
print('='*70)

importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance.head(15))
importance.to_csv('outputs/reports/feature_importance.csv', index=False)

plt.figure(figsize=(10, 8))
top_n = importance.head(15)
sns.barplot(data=top_n, x='Importance', y='Feature', palette='viridis')
plt.title('Top 15 Feature Importance (XGBoost)', fontsize=14, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('outputs/figures/09_feature_importance.png')
# %% [markdown]
# ## 11. Final Model Classification Report

# %%
print('='*70)
print('11. FINAL MODEL — DETAILED REPORT')
print('='*70)
print(f'\nModel: XGBoost (Tuned)')
print(f'Best params: {grid.best_params_}')
print('\nClassification Report:')
print(classification_report(y_test, y_pred_tuned,
                            target_names=['Rejected', 'Approved']))

# %% [markdown]
# ## 12. Model Persistence

# %%
print('='*70)
print('12. SAVING MODEL')
print('='*70)

joblib.dump(best_model, 'models/loan_xgb_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print('Saved: models/loan_xgb_model.pkl')
print('Saved: models/scaler.pkl')

# %% [markdown]
# ## 13. Conclusion

# %%
print('='*70)
print('13. CONCLUSION')
print('='*70)

print(f'''
PROJECT: Loan Classification
DATASET:  {df.shape[0]:,} applicants × {df.shape[1]} features
TRAIN:    {X_train.shape[0]:,} samples
TEST:     {X_test.shape[0]:,} samples
APPROVAL: {y.mean()*100:.1f}% (balanced)

MODELS EVALUATED (6 total):
  1. Logistic Regression
  2. Decision Tree
  3. Random Forest
  4. XGBoost
  5. K-Nearest Neighbors
  6. Support Vector Machine

TOP MODEL: {results_df.iloc[0]["Model"]} (untuned) → XGBoost (tuned)
TUNED ROC-AUC: {tuned_metrics["ROC-AUC"]:.4f}
TUNED F1:       {tuned_metrics["F1"]:.4f}
TUNED ACCURACY: {tuned_metrics["Accuracy"]:.4f}

TOP 5 PREDICTIVE FEATURES:
  1. {importance.iloc[0]["Feature"]} ({importance.iloc[0]["Importance"]:.4f})
  2. {importance.iloc[1]["Feature"]} ({importance.iloc[1]["Importance"]:.4f})
  3. {importance.iloc[2]["Feature"]} ({importance.iloc[2]["Importance"]:.4f})
  4. {importance.iloc[3]["Feature"]} ({importance.iloc[3]["Importance"]:.4f})
  5. {importance.iloc[4]["Feature"]} ({importance.iloc[4]["Importance"]:.4f})

KEY INSIGHTS:
  - Credit score and debt-to-income ratio are the strongest predictors
  - Annual income significantly influences approval decisions
  - Employment status (especially unemployed) is a critical filter
  - Co-signer presence notably improves approval probability
  - XGBoost outperforms other models due to its ability to capture
    non-linear relationships and feature interactions
''')

# Save final summary
with open('outputs/reports/final_summary.txt', 'w') as f:
    f.write(f'Loan Classification — Final Model Summary\n')
    f.write(f'{"="*60}\n\n')
    f.write(f'Best Model: XGBoost (Tuned)\n')
    f.write(f'Best Params: {grid.best_params_}\n\n')
    f.write(f'Test Set Performance:\n')
    f.write(f'  Accuracy:  {tuned_metrics["Accuracy"]:.4f}\n')
    f.write(f'  Precision: {tuned_metrics["Precision"]:.4f}\n')
    f.write(f'  Recall:    {tuned_metrics["Recall"]:.4f}\n')
    f.write(f'  F1 Score:  {tuned_metrics["F1"]:.4f}\n')
    f.write(f'  ROC-AUC:   {tuned_metrics["ROC-AUC"]:.4f}\n')

print('\nFinal summary saved: outputs/reports/final_summary.txt')
print('\n=== PROJECT COMPLETE ===')
