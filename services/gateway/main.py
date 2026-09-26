import httpx, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Assessment 4 ML Gateway",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "fraud": os.getenv(
        "FRAUD_SERVICE_URL",
        "http://fraud-service.fraud.svc.cluster.local"
    ),
    "recommendations": os.getenv(
        "RECOMMENDATIONS_SERVICE_URL",
        "http://recommendations-service.recommendations.svc.cluster.local"
    ),
    "forecasting": os.getenv(
        "FORECASTING_SERVICE_URL",
        "http://forecasting-service.forecasting.svc.cluster.local"
    ),
}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "gateway"}


@app.get("/services")
async def service_status():
    results = {}

    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in SERVICES.items():
            try:
                response = await client.get(f"{url}/health")
                response.raise_for_status()

                results[name] = {
                    "status": "healthy",
                    "url": url
                }

            except Exception:
                results[name] = {
                    "status": "unhealthy",
                    "url": url
                }

    return results


@app.post("/predict/{service}")
async def predict(service: str, payload: dict):
    if service not in SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown service: {service}"
        )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{SERVICES[service]}/predict",
                json=payload
            )

            response.raise_for_status()
            return response.json()

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"{service} service failed: {str(e)}"
        )