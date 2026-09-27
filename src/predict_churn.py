import pandas as pd
from pathlib import Path
import joblib

project_folder = Path(__file__).resolve().parent.parent
model_path = project_folder / 'models' / 'churn_model.joblib'

model = joblib.load(model_path)

new_customer = pd.DataFrame([{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 80.5,
    "TotalCharges": 966.0
}])

prediction = model.predict(new_customer)
probability = model.predict_proba(new_customer)[0][1]

print('Churn probability is ', round(probability * 100, 2), '%')
if prediction[0] == 1:
    print('Customer is likely to churn.')
else:
    print('Customer is likely to stay.')