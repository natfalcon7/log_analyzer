import re 

# Relative path to the log file
LOG_PATH = "./logs.txt"


errors =[]
# Read the log file line by line using a generate to save memory.

def load_logs():

	try:
		with open(LOG_PATH,"r") as file:
			for line in file:
				yield line.strip()

	except Exception as e:
		errors.append(f"File error: {e}")


# Ensures the line is not empty.

def validate_non_emppty_line(line):
	try:
		if len(line) > 0:
			return line 
	except Exception as e:
		errors.append(f"Line empty: {e}")
	return None	


# Validates and parses a log line into timestamp, user and event.
# Expected format:
# YYYY-MM-DD HH:MM:SS(.microseconds) | user | event

def parse_log_line(line):
	parts = line.split("|")
	
	timestamp_pattern = r"^\d{4}[-/.]\d{2}[-/.]\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?$"
	user_pattern = r"[a-zA-Z0-9_-]+"
	event_pattern =r".+"

	if len(parts) != 3:
		errors.append(f"Invalid log structure")
		return None
	
	timestamp, user, event = parts

	timestamp = timestamp.strip()
	user = user.strip()
	event = event.strip()


	if not re.fullmatch(timestamp_pattern,timestamp.strip()):
		errors.append(f"Invalid timestamp: {timestamp}")

		return None

	if not re.fullmatch(user_pattern,user.strip()):
		errors.append(f"Invalid user: {user}")

		return None

	if not re.fullmatch(event_pattern,event.strip()):
		errores.append(f"Mensaje vacío o inválido: {message}")

		return None		

	return timestamp.strip(), user.strip(), event.strip()

def extract_hour(timestamp):
	return timestamp[11:13]

		
#-----------------------Main flow--------------------------------------------------------------

parsed_logs =[]

if __name__ == '__main__':
	
	for line in load_logs():

		clean_line = validate_non_emppty_line(line)
		if not clean_line:
			continue

		parsed = parse_log_line(clean_line)
		if parsed:
			parsed_logs.append(parsed)

#-------------Análysis------------------------------------------------------------------------------


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
	timestamp, user, type = log
	hour = extract_hour(timestamp)

	# Global count
	logs_for_user[user]= logs_for_user.get(user, 0) + 1
	logs_for_type[type]= logs_for_type.get(type, 0) + 1

	# Events by hour
	events_by_hour[hour] = events_by_hour.get(hour, 0) +1

	# Error by hour
	if type in ["error_404", "error_500"]:
		error_by_hour[hour] = error_by_hour.get(hour, 0) +1

	# Activity user/hour
	if user not in activity_user_by_hour:
		activity_user_by_hour[user] = {}
	activity_user_by_hour[user][hour] = activity_user_by_hour[user].get(hour, 0) +1

	# whoe makes more errors?
	if type in ["error_404", "error_500"]:
		error_by_user[user] = error_by_user.get(user, 0) +1
		
		
		# Errors by user/hour
		if user not in errors_user_by_hour:
			errors_user_by_hour[user] = {}
		errors_user_by_hour[user][hour] = errors_user_by_hour[user].get(hour, 0) +1	

user_more_errors = max(error_by_user, key= error_by_user.get)

# Unusual spikes in activity
unusual_spikes = {}
for user, hours in activity_user_by_hour.items():
	spikes = {h: c for h, c in hours.items() if c>10}
	if spikes:
		unusual_spikes[user] = spikes
 
# Peak unusual activity per user
for user, hours in activity_user_by_hour.items():
	max_events = 0
	peak_hour = None

	for hour, events in hours.items():
		if events > max_events:
			max_events = events
			peak_hour = hour

	max_activity_per_user[user] = {"hour": peak_hour, "events": max_events}
	
# Correlation: errors during peak activity of user with most errors
peak_hour_user_more_errors = max_activity_per_user[user_more_errors]["hour"]

errors_in_peak = 0
if user_more_errors in errors_user_by_hour:
	errors_in_peak = errors_user_by_hour[user_more_errors].get(peak_hour_user_more_errors, 0)




total_events = sum(logs_for_user.values())
most_active_user = max(logs_for_user, key=logs_for_user.get)
most_frequent_event = max(logs_for_type, key=logs_for_type.get)
top3_event = sorted(logs_for_type.items(),key= lambda x: x[1], reverse= True)[:3]
top3_users = sorted(logs_for_user.items(),key= lambda x: x[1], reverse= True)[:3]

# Top info
summary = {
	"most_active_user": most_active_user, 
	"user_with_most_errors": user_more_errors,
	"peak_hour_of_problem_user": peak_hour_user_more_errors,
	"errors_in_peak": errors_in_peak,
	"top3_users": top3_users,
	"top3_events": top3_event,
}

print(summary)
