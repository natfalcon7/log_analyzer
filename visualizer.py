# visualizer.py
# Responsible for exporting the summary to JSON or CSV.

import json
import csv


def export(summary, path, format):
    
    #Exports the summary dictionary to a file.
    #format: 'json' or 'csv'
    
    if format == "json":
        with open(path, "w") as f:
            json.dump(summary, f, indent=4)
        print(f"Report exported to {path}")

    elif format == "csv":
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["field", "value"])
            for key, value in summary.items():
                writer.writerow([key, value])
        print(f"Report exported to {path}")

    else:
        print(f"Unknown format: {format}. Use 'json' or 'csv'.")
