from pathlib import Path
import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


project_folder = Path(__file__).resolve().parent.parent
model_path = project_folder / "models" / "churn_model.joblib"

model = joblib.load(model_path)

app = FastAPI(title="Customer Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}


@app.post("/predict")
def predict_churn(customer: CustomerData):
    prediction_data = pd.DataFrame([customer.model_dump()])

    prediction = model.predict(prediction_data)
    probability = model.predict_proba(prediction_data)[0][1]

    if prediction[0] == 1:
        result = "Customer is likely to churn."
    else:
        result = "Customer is likely to stay."

    return {
        "churn_probability": round(probability * 100, 2),
        "prediction": result
    }