# analyzer.py
# Responsible for computing all statistics from parsed logs.

from parser import extract_hour


def analyze(parsed_logs):
    
    #Receives a list of (timestamp, user, event) tuples.
    #Returns a dictionary with all computed statistics.
    
    logs_for_user = {}
    logs_for_type = {}
    events_by_hour = {}
    error_by_hour = {}
    activity_user_by_hour = {}
    error_by_user = {}
    max_activity_per_user = {}
    errors_user_by_hour = {}
    errors_by_user_and_type = {}

    for log in parsed_logs:
        timestamp, user, event_type = log
        hour = extract_hour(timestamp)

        # Global count
        logs_for_user[user] = logs_for_user.get(user, 0) + 1
        logs_for_type[event_type] = logs_for_type.get(event_type, 0) + 1

        # Events by hour
        events_by_hour[hour] = events_by_hour.get(hour, 0) + 1

        # Errors by hour
        if event_type in ["error_404", "error_500"]:
            error_by_hour[hour] = error_by_hour.get(hour, 0) + 1

        # Activity per user per hour
        if user not in activity_user_by_hour:
            activity_user_by_hour[user] = {}
        activity_user_by_hour[user][hour] = activity_user_by_hour[user].get(hour, 0) + 1

        # Errors per user
        if event_type in ["error_404", "error_500"]:
            error_by_user[user] = error_by_user.get(user, 0) + 1

            # Errors per user per hour
            if user not in errors_user_by_hour:
                errors_user_by_hour[user] = {}
            errors_user_by_hour[user][hour] = errors_user_by_hour[user].get(hour, 0) + 1

            # Errors per user per type
            if user not in errors_by_user_and_type:
                errors_by_user_and_type[user] = {}
            errors_by_user_and_type[user][event_type] = errors_by_user_and_type[user].get(event_type, 0) + 1

    # User with most errors
    user_more_errors = max(error_by_user, key=error_by_user.get)

    # Unusual spikes in activity
    unusual_spikes = {}
    for user, hours in activity_user_by_hour.items():
        avg_activity = sum(hours.values()) / len(hours)
        threshold = max(avg_activity * 1.3, avg_activity + 5)
        spikes = {h: c for h, c in hours.items() if c > threshold}
        if spikes:
            unusual_spikes[user] = {
                "average_activity": round(avg_activity, 2),
                "threshold_used": round(threshold, 2),
                "spike_hours": spikes
            }

    # Peak activity hour per user
    for user, hours in activity_user_by_hour.items():
        max_events = 0
        peak_hour = None
        for hour, events in hours.items():
            if events > max_events:
                max_events = events
                peak_hour = hour
        max_activity_per_user[user] = {"hour": peak_hour, "events": max_events}

    # Correlation: errors during peak hour of problem user
    peak_hour_user_more_errors = max_activity_per_user[user_more_errors]["hour"]
    errors_in_peak = 0
    if user_more_errors in errors_user_by_hour:
        errors_in_peak = errors_user_by_hour[user_more_errors].get(peak_hour_user_more_errors, 0)

    # Time with most errors vs time with most activity
    hour_most_errors = max(error_by_hour, key=error_by_hour.get)
    hour_most_events = max(events_by_hour, key=events_by_hour.get)
    if hour_most_errors == hour_most_events:
        error_vs_activity = "The time with most errors is the same as the time with most activity."
    else:
        error_vs_activity = "The time with most errors is different from the time with most activity."

    # Problem user vs system peak hour
    system_peak_hour = max(events_by_hour, key=events_by_hour.get)
    errors_in_system_peak = errors_user_by_hour.get(user_more_errors, {}).get(system_peak_hour, 0)
    total_errors_user = error_by_user[user_more_errors]
    avg_errors_other_hours = total_errors_user / len(events_by_hour)

    if errors_in_system_peak > avg_errors_other_hours:
        problemUser_vs_systemPeak = f"{user_more_errors} generates more errors when the system is at peak hour {system_peak_hour}"
    else:
        problemUser_vs_systemPeak = f"{user_more_errors} generates more errors when the system is quiet"

    # Global summaries
    total_events = sum(logs_for_user.values())
    most_active_user = max(logs_for_user, key=logs_for_user.get)
    most_frequent_event = max(logs_for_type, key=logs_for_type.get)
    top3_events = sorted(logs_for_type.items(), key=lambda x: x[1], reverse=True)[:3]
    top3_users = sorted(logs_for_user.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "total_events": total_events,
        "most_active_user": most_active_user,
        "most_frequent_event": most_frequent_event,
        "system_peak_hour": system_peak_hour,
        "top3_users": top3_users,
        "top3_events": top3_events,
        "user_more_errors": user_more_errors,
        "peak_hour_user_more_errors": peak_hour_user_more_errors,
        "errors_in_peak": errors_in_peak,
        "errors_in_system_peak": errors_in_system_peak,
        "avg_errors_other_hours": avg_errors_other_hours,
        "error_vs_activity": error_vs_activity,
        "problemUser_vs_systemPeak": problemUser_vs_systemPeak,
        "unusual_spikes": unusual_spikes,
        "errors_by_user_and_type": errors_by_user_and_type,
        "max_activity_per_user": max_activity_per_user,
        "events_by_hour": events_by_hour,
        "error_by_hour": error_by_hour,
    }