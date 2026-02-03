## Log Analyzer - Python (Version 1.0)

A **pure Python** log analyzer that processes system activity logs, detects relevants patterns, and generates **metrics + automatic alerts** based on logical rules.

This project was developed as a practical exercise to learn:

- safe file reading
- regex validation
- log parsing
- aggregations by user and hour
- simple correlations
- unusual spike detection
- automatic alert generation

 **Project focus: ** rule-based logical analysis (not machine learning).
------------------------------------------------------

# Expected log format

Each line in "logs.txt" should follow this format:

YYYY-MM-DD HH:MM:SS(.microseconds) | user |event

valid example: 

2026-01-27 18:32:10.345123 | alice | error_404

------------------------------------------------------
# How to run

1. Place your "logs.txt" file in the same folder as the script.
2. Run:
````
python simple_log_analyzer.py
````
The program prints a structured summary using pprint.

------------------------------------------------------
# Log Generator (included in the repository)

This project includes a Python script (`generate_logs.py`) that creates synthetic log data 
for testing and demonstration purposes. The generator is designed to produce logs that 
match exactly the format expected by the analyzer.

## What the generator does

The generator:

- Creates a file named `logs.txt`
- Produces a configurable number of log lines (`NUM_LINES`)
- Simulates a realistic time flow by increasing timestamps every 1–5 seconds
- Randomly assigns users and events from predefined lists
- Intentionally injects noisy/invalid lines (8%) to test the robustness of the analyzer

### Configurable parameters

Inside `log_generator.py` you can modify:

```python
NUM_LINES = 12000          # number of logs to generate
NOISE_PROBABILITY = 0.08   # percentage of invalid lines
```
You can also adjust the list of users or events if needed.

# How to run the generator

python log_generator.py

+ This will overwrite logs.txt with a new dataset.
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
* Errors per user and type(404, 500)
* Peak hour of the problem user

*Correlations and behavior*
* Does the hour with most match the hour with most activity?
* Does the problem user fail more when the system is at peak?

*Unusual spike detection*
* Detects abnormally high activity hours per user using:

threshold = max(avg * 1.3, avg + 5)
-------------------------------------------------------------

# Alert system 

*An automatic alert is generated if:*
* The user with most errors has:
-at least 30% more errors than their average, 
-at least 20 errors during the system peak hour.

Otherwise, normal behavior is reported.   
-------------------------------------------------------------

## REAL output example ##
{
 'total_events_processed': 11036,
 'most_active_user': 'frank',
 'most_frequent_event': 'password_change',
 'system_peak_hour': '18',

 'top3_users': [('frank', 1158), ('carla', 1130), ('irene', 1122)],
 'top3_events': [('password_change', 1623),
                 ('login', 1583),
                 ('logout', 1581)],

 'user_with_most_errors': 'alice',
 'peak_hour_of_problem_user': '22',
 'errors_in_user_peak': 40,
 'errors_in_system_peak': 52,

 'problemUser_vs_systemPeak':
   'alice generates more errors when the system is at peak 18',

 'error_vs_activity':
   'The time with most errors is the same as the time the most activity.',

 'unusual_spikes': {
    'carla': {
        'average_activity': 113.0,
        'threshold_used': 146.9,
        'spike_hours': {'01': 150}
    }
 },

 'errors_by_user_and_type': {
    'alice': {'error_404': 174, 'error_500': 160},
    'peak_hour_user_more_errors': '22'
 },

 'peak_activity_per_user': {
    'alice': {'events': 139, 'hour': '22'},
    'frank': {'events': 140, 'hour': '22'},
    'carla': {'events': 150, 'hour': '01'}
 },

 'events_by_hour': {'18': 1201, '21': 1186, ...},
 'errors_by_hour': {'18': 359, '22': 332, ...},

 'alert':
  'ALERTA: alice generates 1.56x more errors than usual during peak system hours(18).'
}

# Note:
The results of the analysis may vary each time the program is executed if new logs are generated, 
since the included log dataset is randomly produced by a separate log generator. Different input data 
naturally leads to different statistics, rankings, and alerts.


------------------------------------------------------------

# Possible future improvements

+ Export results to CSV or JSON
+ Generate hourly charts
+ Detect patterns by day
+ Add more types of alerts
+ Read logs as streaming data
# ------------------------------------------------------------

### AUTHOR ###

# Flores Falcón Natanael Emanuel.-