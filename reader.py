# reader.py
# Responsible for loading the log file and filtering empty lines.

LOG_PATH = "./logs.txt"

errors = []


def load_logs():
    #Read the log file line by line using a generator to save memory.
    try:
        with open(LOG_PATH, "r") as file:
            for line in file:
                yield line.strip()
    except Exception as e:
        errors.append(f"File error: {e}")


def validate_non_empty_line(line):
    #Ensures the line is not empty.
    if line and len(line) > 0:
        return line
    return None