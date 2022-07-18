from datetime import datetime, timedelta, timezone


def utc_now():
    """Current UTC date and time"""
    return datetime.now(timezone.utc)
