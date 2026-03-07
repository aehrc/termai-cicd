from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_expected_payload() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert "time" in body
    assert isinstance(body["time"], str)

    parsed = datetime.fromisoformat(body["time"])
    assert parsed is not None
    assert parsed.utcoffset() == datetime.now(ZoneInfo("Australia/Sydney")).utcoffset()
