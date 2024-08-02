import re
from datetime import timedelta

import inflect


# Copied and tweaked from https://gist.github.com/spatialtime/c1924a3b178b4fe721fe406e0bf1a1dc#file-iso8601_duration-py
def iso_to_timedelta(iso_duration: str) -> timedelta:
    m = re.match(
        r"^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:.\d+)?)S)?$",
        iso_duration,
    )
    if m is None:
        raise ValueError("invalid ISO 8601 duration string")

    days = 0
    hours = 0
    minutes = 0
    seconds = 0.0

    # Years and months are not being utilized here, as there is not enough
    # information provided to determine which year and which month.
    # Python's time_delta class stores durations as days, seconds and
    # microseconds internally, and therefore we'd have to
    # convert parsed years and months to specific number of days.

    if m[3]:
        days = int(m[3])
    if m[4]:
        hours = int(m[4])
    if m[5]:
        minutes = int(m[5])
    if m[6]:
        seconds = float(m[6])

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


# Copied and tweaked from https://gist.github.com/thatalextaylor/7408395
def pretty_timedelta(duration: timedelta, lang=inflect.engine()):
    seconds = duration.total_seconds()
    if not seconds:
        return f"0 seconds"
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    measures = (
        (days, "day"),
        (hours, "hour"),
        (minutes, "minute"),
        (seconds, "second"),
    )
    return lang.join(
        [f"{count} {lang.plural(noun, count)}" for (count, noun) in measures if count]
    )
