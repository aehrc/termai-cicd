from fastapi import FastAPI

from app.services.health_service import build_health_payload

app = FastAPI(title="Health Service")


@app.get("/health")
def health() -> dict[str, str]:
    return build_health_payload()
