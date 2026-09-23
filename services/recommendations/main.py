import os
import boto3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Recommendations Service",
    version="1.0.0"
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SAGEMAKER_ENDPOINT = os.getenv(
    "SAGEMAKER_ENDPOINT",
    "assessment4-ying-recommendations-endpoint"
)

sagemaker_runtime = boto3.client(
    "sagemaker-runtime",
    region_name=AWS_REGION
)


class RecommendationRequest(BaseModel):
    user_id: int
    product_id: int
    user_activity_score: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "recommendations"
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
        "service": "recommendations"
    }


@app.post("/predict")
def predict(request: RecommendationRequest):
    try:
        payload = (
            f"{request.user_id},"
            f"{request.product_id},"
            f"{request.user_activity_score}"
        )

        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType="text/csv",
            Body=payload
        )

        result = response["Body"].read().decode("utf-8")
        recommendation_score = float(result)

        return {
            "recommendation_score": recommendation_score,
            "recommended": recommendation_score >= 0.5,
            "endpoint": SAGEMAKER_ENDPOINT
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SageMaker inference failed: {str(e)}"
        )