def humanize_time_difference(seconds):
    seconds = int(seconds)

    # Future or Past
    if seconds < 0:
        suffix = "ago"
        seconds = abs(seconds)
    else:
        suffix = "in"

    # Time thresholds
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day

    if seconds < minute:
        value = seconds
        unit = "second"
    elif seconds < hour:
        value = seconds // minute
        unit = "minute"
    elif seconds < day:
        value = seconds // hour
        unit = "hour"
    elif seconds < week:
        value = seconds // day
        unit = "day"
    else:
        value = seconds // week
        unit = "week"

    # Handle plural
    if value != 1:
        unit += "s"

    if suffix == "ago":
        return f"{value} {unit} ago"
    else:
        return f"in {value} {unit}"
