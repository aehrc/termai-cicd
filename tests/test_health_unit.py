from datetime import datetime

from app.services.health_service import build_health_payload


def test_build_health_payload_shape_and_values() -> None:
    payload = build_health_payload()

    assert payload["status"] == "ok"
    assert "time" in payload
    assert isinstance(payload["time"], str)

    parsed = datetime.fromisoformat(payload["time"])
    assert parsed is not None
