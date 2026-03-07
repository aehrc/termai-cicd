from datetime import datetime
from zoneinfo import ZoneInfo


SYDNEY_TZ = ZoneInfo("Australia/Sydney")


def build_health_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "time": datetime.now(SYDNEY_TZ).isoformat(),
    }
