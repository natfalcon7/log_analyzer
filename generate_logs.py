import random
from datetime import datetime, timedelta


# Configuración general


NUM_LINES = 12000
OUTPUT_FILE = "logs.txt"

USERS = [
    "alice", "bob", "carla", "daniel", "eva",
    "frank", "gina", "hector", "irene", "juan"
]

EVENTS = [
    "login",
    "logout",
    "view_page",
    "click_button",
    "error_404",
    "error_500",
    "password_change"
]

NOISE_PROBABILITY = 0.08  # 8% de líneas con ruido



# Generadores auxiliares


def generate_timestamp(current_time):
    # Avanza el tiempo entre 1 y 5 segundos
    delta = timedelta(seconds=random.randint(1, 5))
    return current_time + delta


def generate_valid_log(timestamp):
    user = random.choice(USERS)
    event = random.choice(EVENTS)
    return f"{timestamp} | {user} | {event}"


def generate_noise():
    noise_types = [
        "",  # línea vacía
        "THIS IS NOT A LOG LINE",
        "2024-13-99 99:99:99 | alice",
        "||",
        "2024-05-01 12:00:00 - bob - login",
        "2024-05-01 12:00:00 | | login",
        "random text with no meaning"
    ]
    return random.choice(noise_types)



# Generación del archivo


def generate_log_file():
    current_time = datetime.now()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for _ in range(NUM_LINES):
            if random.random() < NOISE_PROBABILITY:
                line = generate_noise()
            else:
                current_time = generate_timestamp(current_time)
                line = generate_valid_log(current_time)

            file.write(line + "\n")


if __name__ == "__main__":
    generate_log_file()
    print(f"Archivo '{OUTPUT_FILE}' generado con {NUM_LINES} líneas.")
