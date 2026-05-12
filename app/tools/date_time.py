from datetime import datetime
from zoneinfo import ZoneInfo


def current_datetime(timezone: str = "Asia/Kolkata") -> str:
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception:
        now = datetime.now(ZoneInfo("UTC"))
        timezone = "UTC"
    return now.strftime(f"%Y-%m-%d %H:%M:%S {timezone}")
