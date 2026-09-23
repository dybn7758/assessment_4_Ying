import os
import boto3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Forecasting Service",
    version="1.0.0"
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SAGEMAKER_ENDPOINT = os.getenv(
    "SAGEMAKER_ENDPOINT",
    "assessment4-ying-forecasting-endpoint"
)

sagemaker_runtime = boto3.client(
    "sagemaker-runtime",
    region_name=AWS_REGION
)


class ForecastRequest(BaseModel):
    previous_day_sales: float
    seven_day_average: float
    day_of_week: int


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "forecasting"
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
        "service": "forecasting"
    }


@app.post("/predict")
def predict(request: ForecastRequest):
    try:
        payload = (
            f"{request.previous_day_sales},"
            f"{request.seven_day_average},"
            f"{request.day_of_week}"
        )

        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType="text/csv",
            Body=payload
        )

        result = response["Body"].read().decode("utf-8")
        forecast = float(result)

        return {
            "forecast": forecast,
            "endpoint": SAGEMAKER_ENDPOINT
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SageMaker inference failed: {str(e)}"
        )