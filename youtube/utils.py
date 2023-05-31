import re
import datetime

def parse_duration(duration):
    match = re.match(r"PT(\d+H)?(\d+M)?(\d+S)?", duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def get_delta(published_at):
    start_datetime = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    end_datetime = datetime.datetime.now()
    time_difference = end_datetime - start_datetime
    time_difference_hours = int(round(time_difference.total_seconds() / 3600))

    return time_difference_hours