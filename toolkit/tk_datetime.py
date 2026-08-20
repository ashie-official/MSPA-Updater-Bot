from datetime import (
    date as dt_date,
    time as dt_time,
    datetime as dt_datetime,
    timezone as dt_timezone,
)

################################################################################################################################


TIMEZONE = dt_timezone.utc


################################################################################################################################


def now():
    return dt_datetime.now(TIMEZONE)


def get_difference(end: dt_datetime, start: dt_datetime = now()):
    return (end - start).total_seconds()


def timezone_str(dt: dt_datetime | str, format: str = "f") -> str:
    """
    Takes a dt_datetime object or ISO-formatted string and returns a Discord timezone-adjusting string.

    Formats:

    (Default) f, Short Date/Time: `"May 26, 2026 5:00 PM"`

    F, Long Date/Time: `"Tuesday, May 26, 2026 5:00 PM"`

    d, Short Date: `05/26/2026`

    D, Long Date: `"May 26, 2026"`

    t, Short Time: `5:00 PM`

    T, Long Time: `5:00:00 PM`

    R, Relative Time: `in 5 minutes` / `2 hours ago`
    """

    if isinstance(dt, dt_datetime):
        return f"<t:{int(dt.timestamp())}:{format}>"
    if isinstance(dt, str):
        return f"<t:{int(dt_datetime.fromisoformat(dt).timestamp())}:{format}>"


def parse_date(value: str, format: str = "%m/%d") -> dt_date:
    """Basically just an alias for passing dates through datetime.strptime(), default format `MM/DD`"""
    parsed_dt = dt_datetime.strptime(value, format)
    return parsed_dt.date()


def parse_time(value: str, format: str = "%H:%M") -> dt_time:
    """Basically just an alias for passing times through datetime.strptime(), default format `HH:MM`"""
    parsed_dt = dt_datetime.strptime(value, format)
    return parsed_dt.time()
