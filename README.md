## Log Analyzer - Python (Version 2.0)

A **pure Python** log analyzer that processes system activity logs, detects relevant patterns, and generates **metrics + automatic alerts** based on logical rules.

This project was developed as a practical exercise to learn:

- safe file reading
- regex validation
- log parsing
- aggregations by user and hour
- simple correlations
- unusual spike detection
- automatic alert generation
- modular project architecture
- export to JSON and CSV

 **Project focus:** rule-based logical analysis (not machine learning).
------------------------------------------------------

# Project structure

    reader.py       — loads the log file and filters empty lines
    parser.py       — validates and parses each log line
    analyzer.py     — computes all statistics and correlations
    alerts.py       — generates alerts based on analysis results
    visualizer.py   — exports the report to JSON or CSV
    main.py         — orchestrator: coordinates all modules
    generate_logs.py — synthetic log generator for testing

------------------------------------------------------

# Expected log format

Each line in "logs.txt" should follow this format:

YYYY-MM-DD HH:MM:SS(.microseconds) | user | event

valid example:

2026-01-27 18:32:10.345123 | alice | error_404

------------------------------------------------------
# How to run

1. Place your "logs.txt" file in the same folder as the scripts.
2. Run:

    python main.py

The program prints a structured summary using pprint.

To export the report to a file:

    python main.py --output report.json
    python main.py --output report.csv --format csv

------------------------------------------------------
# Log Generator (included in the repository)

This project includes a Python script (`generate_logs.py`) that creates synthetic log data
for testing and demonstration purposes. The generator is designed to produce logs that
match exactly the format expected by the analyzer.

## What the generator does

The generator:

- Creates a file named `logs.txt`
- Produces a configurable number of log lines (`NUM_LINES`)
- Simulates a realistic time flow by increasing timestamps every 1-5 seconds
- Randomly assigns users and events from predefined lists
- Intentionally injects noisy/invalid lines (8%) to test the robustness of the analyzer

### Configurable parameters

Inside `generate_logs.py` you can modify:

    NUM_LINES = 12000          # number of logs to generate
    NOISE_PROBABILITY = 0.08   # percentage of invalid lines

You can also adjust the list of users or events if needed.

# How to run the generator

    python generate_logs.py

This will overwrite logs.txt with a new dataset.
Because the data is random, different runs will lead to different analysis results.

-------------------------------------------------------
# What the program analyzes

*Global system stats*
* Total events processed
* Most active user
* Most frequent event
* System peak hour

*Rankings*
* Top 3 most active users
* Top 3 most frequent events

*Error analysis*
* User with most errors
* Errors per system hour
* Errors per user and type (404, 500)
* Peak hour of the problem user

*Correlations and behavior*
* Does the hour with most errors match the hour with most activity?
* Does the problem user fail more when the system is at peak?

*Unusual spike detection*
* Detects abnormally high activity hours per user using:

    threshold = max(avg * 1.3, avg + 5)

-------------------------------------------------------------

# Alert system

*An automatic alert is generated if:*
* The user with most errors has:
- at least 30% more errors than their average,
- at least 20 errors during the system peak hour.

Otherwise, normal behavior is reported.
-------------------------------------------------------------

## REAL output example ##

    {'alert': "OK: carla's behavior doesn't show an abnormal spike in errors "
              "during the system's peak hour.",
     'error_vs_activity': 'The time with most errors is the same as the time '
                          'with most activity.',
     'errors_by_hour': {'00': 357, '01': 341, '02': 352, '03': 299, '23': 374},
     'errors_by_user_and_type': {'alice': {'error_404': 159, 'error_500': 143},
                                 'carla': {'error_404': 173, 'error_500': 157}},
     'errors_in_system_peak': 39,
     'errors_in_user_peak': 44,
     'events_by_hour': {'00': 1190, '01': 1219, '23': 1224},
     'most_active_user': 'carla',
     'most_frequent_event': 'logout',
     'peak_activity_per_user': {'carla': {'events': 149, 'hour': '01'},
                                'irene': {'events': 150, 'hour': '20'}},
     'peak_hour_of_problem_user': '01',
     'problemUser_vs_systemPeak': 'carla generates more errors when the system '
                                  'is at peak hour 23',
     'system_peak_hour': '23',
     'top3_events': [('logout', 1628), ('error_404', 1608), ('click_button', 1594)],
     'top3_users': [('carla', 1118), ('bob', 1114), ('irene', 1113)],
     'total_events_processed': 11015,
     'unusual_spikes': {'carla': {'average_activity': 111.8,
                                  'spike_hours': {'01': 149},
                                  'threshold_used': 145.34}}}

# Note:
The results of the analysis may vary each time the program is executed if new logs are generated,
since the included log dataset is randomly produced by a separate log generator. Different input data
naturally leads to different statistics, rankings, and alerts.

------------------------------------------------------------

# Changelog

Version 2.0
- Refactored into modular architecture (reader, parser, analyzer, alerts, visualizer, main)
- Added export to JSON and CSV via --output and --format arguments
- Fixed naming inconsistencies in error handling
- Improved code readability and separation of responsibilities

Version 1.0
- Single-file implementation
- Core analysis, spike detection and alert system

------------------------------------------------------------

### AUTHOR ###

# Flores Falcon Natanael Emanuel.-