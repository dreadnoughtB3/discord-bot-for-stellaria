from datetime import datetime
from zoneinfo import ZoneInfo

def get_japan_current_time() -> datetime:
    japan_tz = ZoneInfo("Asia/Tokyo")
    return datetime.now(japan_tz)