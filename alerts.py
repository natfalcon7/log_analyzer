# alerts.py
# Responsible for generating alerts based on analysis results.

ERROR_SPIKE_THRESHOLD = 1.3 # 30% more than average
MIN_ERRORS_TO_ALERT = 20


def generate_alert(user_more_errors, errors_in_system_peak, avg_errors_other_hours, system_peak_hour):
    
    #Evaluates error behavior and returns an alert message string.
    
    if (errors_in_system_peak > avg_errors_other_hours * ERROR_SPIKE_THRESHOLD
            and errors_in_system_peak >= MIN_ERRORS_TO_ALERT):
        return (
            f"ALERT: {user_more_errors} generates "
            f"{round(errors_in_system_peak / avg_errors_other_hours, 2)}x "
            f"more errors than usual during peak system hours ({system_peak_hour})."
        )
    else:
        return (
            f"OK: {user_more_errors}'s behavior "
            f"doesn't show an abnormal spike in errors during the system's peak hour."
        )