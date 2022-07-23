from datetime import datetime, timezone


def utc_now():
    """Current UTC date and time"""
    return datetime.now(timezone.utc)
