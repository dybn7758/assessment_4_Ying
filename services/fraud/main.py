import os
import boto3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Fraud Detection Service",
    version="1.0.0"
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SAGEMAKER_ENDPOINT = os.getenv(
    "SAGEMAKER_ENDPOINT",
    "assessment4-ying-fraud-endpoint"
)

sagemaker_runtime = boto3.client(
    "sagemaker-runtime",
    region_name=AWS_REGION
)


class Transaction(BaseModel):
    amount: float
    transaction_count: int
    account_age_days: int


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "fraud"
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
        "service": "fraud"
    }


@app.post("/predict")
def predict(transaction: Transaction):
    try:
        payload = (
            f"{transaction.amount},"
            f"{transaction.transaction_count},"
            f"{transaction.account_age_days}"
        )

        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType="text/csv",
            Body=payload
        )

        result = response["Body"].read().decode("utf-8")
        fraud_score = float(result)

        return {
            "prediction": (
                "fraud"
                if fraud_score >= 0.5
                else "legitimate"
            ),
            "fraud_score": fraud_score,
            "endpoint": SAGEMAKER_ENDPOINT
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SageMaker inference failed: {str(e)}"
        )