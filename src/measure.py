from src.modules import database
from src.modules.config import Config

from src.modules.sensors.utils import NANO

from src.modules.webui.celery import task_queue

import time
from src.modules.sensor import init_sensor

num_samples = 0
num_proj_samples = 0

CONFIG = Config("config.ini")

from src.modules.database import DB

# Initialize Sensors
SENSORS = {}

for sensor in CONFIG.SENSORS:
    SENSORS[sensor] = init_sensor(CONFIG.SENSORS[sensor])

    if SENSORS[sensor] is None:
        print(sensor + " is NoneType!")
    

# Initialize Celery Task for measurements
@task_queue.task(name="src.measure.measurement_cycle")
def measurement_cycle(site_id, hr, min, sec, num_samples):
    setup()

    target_time = time.time() + sec + (min * 60) + (hr * 3600)
    frequency = ( 1 / num_samples ) * 3600
    num_proj_samples = frequency * 3600

    i = 0
    while (time.time() < target_time):
        loop(site_id, frequency)

    clean_up()
    

def setup():
    # Backup Data Files
    DB.backup()


def loop(site_id, freq):
    # Set target time
    start = time.time()
    end = start + (1 / freq)

    # Get responses from sensors
    responses = {}
    for sensor in SENSORS:
        try:
            responses[sensor] = SENSORS[sensor].read_all()
            print(responses[sensor])
        except:
            print("Error Reading: (" + sensor + ")")

    # Check if target time was hit
    if (time.time() < end):
            print("Hit Target!")
    else:
        print("Missed Target! :(")

    # Record Data to File
    DB.log_data(site_id, responses)

    # Control Box (eg pump)
    pass

    # Wait here until duration has elapsed
    while ((time.time() < end) and (num_samples < num_proj_samples)):
        time.sleep(0.001)


def clean_up():
    # Verify File Integrity?
    pass

if __name__ == "__main__":
    print("DO NOT RUN ME!")
