# main.py
# Orchestrator: coordinates all modules to produce the final report.

import argparse
from pprint import pprint

from reader import load_logs, validate_non_empty_line, errors
from parser import parse_log_line
from analyzer import analyze
from alerts import generate_alert
from visualizer import export


def main():
    # CLI arguments
    arg_parser = argparse.ArgumentParser(description="Log Analyzer")
    arg_parser.add_argument("--output", type=str, help="Path to export the report (e.g. report.json)")
    arg_parser.add_argument("--format", type=str, choices=["json", "csv"], default="json", help="Export format: json or csv")
    args = arg_parser.parse_args()

    # Step 1: Load and parse logs
    parsed_logs = []
    for line in load_logs():
        clean_line = validate_non_empty_line(line)
        if not clean_line:
            continue
        parsed = parse_log_line(clean_line)
        if parsed:
            parsed_logs.append(parsed)

    if not parsed_logs:
        print("No valid logs found. Check your logs.txt file.")
        return

    # Step 2: Analyze
    stats = analyze(parsed_logs)

    # Step 3: Generate alert
    alert_message = generate_alert(
        user_more_errors=stats["user_more_errors"],
        errors_in_system_peak=stats["errors_in_system_peak"],
        avg_errors_other_hours=stats["avg_errors_other_hours"],
        system_peak_hour=stats["system_peak_hour"]
    )

    # Step 4: Build summary
    summary = {
        "total_events_processed": stats["total_events"],
        "most_active_user": stats["most_active_user"],
        "most_frequent_event": stats["most_frequent_event"],
        "system_peak_hour": stats["system_peak_hour"],
        "top3_users": stats["top3_users"],
        "top3_events": stats["top3_events"],
        "user_with_most_errors": stats["user_more_errors"],
        "peak_hour_of_problem_user": stats["peak_hour_user_more_errors"],
        "errors_in_user_peak": stats["errors_in_peak"],
        "errors_in_system_peak": stats["errors_in_system_peak"],
        "problemUser_vs_systemPeak": stats["problemUser_vs_systemPeak"],
        "error_vs_activity": stats["error_vs_activity"],
        "unusual_spikes": stats["unusual_spikes"],
        "errors_by_user_and_type": stats["errors_by_user_and_type"],
        "peak_activity_per_user": stats["max_activity_per_user"],
        "events_by_hour": stats["events_by_hour"],
        "errors_by_hour": stats["error_by_hour"],
        "alert": alert_message,
        "parse_errors": errors
    }

    # Step 5: Display
    pprint(summary)

    # Step 6: Export if requested
    if args.output:
        export(summary, args.output, args.format)


if __name__ == '__main__':
    main()