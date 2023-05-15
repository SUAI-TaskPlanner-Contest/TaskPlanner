from datetime import datetime, timezone
from dateutil.tz import tzlocal


def local_to_utc0(dt: datetime):
    """
        Converts local time to UTC0

        parameters:
            dt (datetime): an awaired/unawaired datetime object with local time
        returns:
            dt (datetime): an awaired datetime object with +00:00 timezone
    """
    return dt.astimezone(timezone.utc)


def utc0_to_local(dt: datetime):
    """
        Converts UTC0 to local time

        parameters:
            dt (datetime): an awaired/unawaired datetime object in UTC0
        returns:
            dt (datetime): an awaired datetime object with local timezone
    """
    return dt.astimezone(tzlocal())
