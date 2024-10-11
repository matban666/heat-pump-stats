from datetime import datetime, timedelta
import pytz

# Get the UTC timezone
utc = pytz.UTC

# Create a timezone-aware datetime.min
datetime_min_aware = datetime.min.replace(tzinfo=utc)
    
def ceil_dt(dt, delta=timedelta(seconds=30)):
    """
    Rounds a datetime object up to the nearest time delta.

    Args:
        dt: The datetime object to round up.
        delta: The timedelta to round up to.

    Returns:
        The rounded datetime object.
    """

    remainder = (dt - datetime_min_aware) % delta
    rounding_offset = (delta - remainder) if remainder else timedelta()
    return dt + rounding_offset