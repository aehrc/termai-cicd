from datetime import datetime, timezone


def build_health_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
    }
