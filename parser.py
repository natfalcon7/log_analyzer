# parser.py
# Responsible for validating and parsing each log line.

import re
from datetime import datetime

from reader import errors


def parse_log_line(line):
    
    #Validates and parses a log line into (timestamp, user, event).
    #Expected format: YYYY-MM-DD HH:MM:SS(.microseconds) | user | event
    #Returns a tuple or None if the line is invalid.
    
    parts = line.split("|")

    timestamp_pattern = r"^\d{4}[-/.]\d{2}[-/.]\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?$"
    user_pattern = r"[a-zA-Z0-9_-]+"
    event_pattern = r".+"

    if len(parts) != 3:
        errors.append("Invalid log structure")
        return None

    timestamp, user, event = parts
    timestamp = timestamp.strip()
    user = user.strip()
    event = event.strip()

    if not re.fullmatch(timestamp_pattern, timestamp):
        errors.append(f"Invalid timestamp: {timestamp}")
        return None

    if not re.fullmatch(user_pattern, user):
        errors.append(f"Invalid user: {user}")
        return None

    if not re.fullmatch(event_pattern, event):
        errors.append(f"Empty or invalid event: {event}")
        return None

    return timestamp, user, event


def extract_hour(timestamp):
    #Extracts the hour (HH) from a timestamp string.
    dt = datetime.fromisoformat(timestamp.replace(" ", "T"))
    return dt.strftime("%H")