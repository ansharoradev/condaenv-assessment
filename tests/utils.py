import time


def current_millis():
    """
    Get the current time in milliseconds.

    Returns:
    int: The current time in milliseconds since the epoch.
    """
    return round(time.time() * 1000)
