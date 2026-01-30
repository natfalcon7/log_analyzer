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

for log in parsed_logs:
	_, user, type = log
	logs_for_user[user]= logs_for_user.get(user, 0) + 1
	logs_for_type[type]= logs_for_type.get(type, 0) + 1

	
total_events = sum(logs_for_user.values())

most_active_user = max(logs_for_user, key=logs_for_user.get)

most_frequent_event = max(logs_for_type, key=logs_for_type.get)

top3_event = sorted(logs_for_type.items(),key= lambda x: x[1], reverse= True)[:3]
top3_users = sorted(logs_for_user.items(),key= lambda x: x[1], reverse= True)[:3]

# prueba visual
print(top3_users)
print(top3_event)
print(most_frequent_event)
print(most_active_user)
print(f"ejemplo: ", {parsed_logs[2]})
print(f"Events per user: {logs_for_user}")
print(f"Events per type: {logs_for_type}")
