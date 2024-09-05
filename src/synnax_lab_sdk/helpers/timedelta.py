from datetime import timedelta

import inflect


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
