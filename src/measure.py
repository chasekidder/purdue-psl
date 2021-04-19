from src.modules import database
from src.modules.config import Config

from src.modules.sensors.utils import NANO

from src.modules.webui.celery import task_queue

import time
from src.modules.sensor import init_sensor


CONFIG = Config("config.ini")

from src.modules.database import DB

# Initialize Sensors
SENSORS = {}

for sensor in CONFIG.SENSORS:
    SENSORS[sensor] = init_sensor(CONFIG.SENSORS[sensor])

# Initialize Celery Task for measurements
@task_queue.task(name="src.measure.measurement_cycle")
def measurement_cycle(duration, frequency):
    setup()

    target_time = time.time() + (60 * duration)

    i = 0
    while (time.time() < target_time):
        loop(frequency)

    clean_up()
    

def setup():
    # Backup Data Files
    DB.backup()


def loop(freq):
    # Set target time
    start = time.time()
    end = start + (1 / freq)

    # Get responses from sensors
    responses = {}
    for sensor in SENSORS:
        responses[sensor] = SENSORS[sensor].read_all()

    # Check if target time was hit
    if (time.time() < end):
            print("Hit Target!")
    else:
        print("Missed Target! :(")

    # Record Data to File
    DB.log_data(responses)

    # Control Box (eg pump)
    pass

    # Wait here until duration has elapsed
    while (time.time() < end):
        time.sleep(0.001)


def clean_up():
    # Verify File Integrity?
    pass

if __name__ == "__main__":
    print("DO NOT RUN ME!")
