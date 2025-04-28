import os
from datetime import date


def get_username() -> str:
    """
    Returns the username of the current user.
    """
    return os.getenv('USER') or os.getenv('USERNAME') or os.getenv('LOGNAME') or ''


def get_date() -> str:
    """
    Returns the current date.
    """
    return date.today().strftime('%d %B %Y')
