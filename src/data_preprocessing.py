import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, 
    accuracy_score, 
    recall_score, 
    precision_score, 
    f1_score
)

project_folder = Path(__file__).resolve().parent.parent
data_path = project_folder / "data" / "Telco-Customer-Churn.csv"

data = pd.read_csv(data_path)

# Convert TotalCharges to numeric
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')

data = data.dropna(subset=['TotalCharges'])
data = data.drop(columns=['customerID'])

# Separate features and target
X = data.drop(columns=['Churn'])
y = data['Churn'].map({'Yes': 1, 'No': 0})


numerical_columns = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]
categorical_columns = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod"
]

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

# Preprocess numerical and categorical features
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_columns),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
])

# Creating preprocessing and model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=100))
])

model.fit(X_train,y_train)

model_path = project_folder / 'models' / 'churn_model.joblib'
joblib.dump(model,model_path)
print('Model saved successfully')

y_pred = model.predict(X_test)

# Evaluate model
print("\nLogistic Regression Pipeline Results:")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Accuracy score:", accuracy_score(y_test, y_pred))
print("Recall score:", recall_score(y_test, y_pred))
print("Precision score:", precision_score(y_test, y_pred))
print("F1 score:", f1_score(y_test, y_pred))

cv_scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=5,
    scoring='f1'
)
print('\nCross Validation F1 Scores : ', cv_scores)
print('Mean Cross Validation F1 : ', cv_scores.mean())

feature_names = model.named_steps['preprocessor'].get_feature_names_out()
coefficient = model.named_steps['classifier'].coef_[0]

feature_importance = pd.DataFrame({
    'Features': feature_names,
    'Coefficient': coefficient
})

feature_importance['Absolute Coefficient'] = feature_importance['Coefficient'].abs()
feature_importance = feature_importance.sort_values(
    'Absolute Coefficient',
    ascending=False
)

print('\nTop 15 important features :')
print(feature_importance.head(15))