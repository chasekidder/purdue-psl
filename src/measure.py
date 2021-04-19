from src.modules import database
from src.modules.config import Config

from src.modules.sensors.utils import NANO

from src.modules.webui.celery import task_queue

import time
from src.modules.sensor import init_sensor


CONFIG = Config("config.ini")

from src.modules.database import DB

# Initialize Sensors

#SENSORS = {
#    "mass flow": init_sensor(CONFIG.SENSORS["mass flow 1"]),
#}
SENSORS = {}

for sensor in CONFIG.SENSORS:
    SENSORS[sensor] = init_sensor(CONFIG.SENSORS[sensor])

@task_queue.task(name="src.measure.measurement_cycle")
def measurement_cycle():
    setup()
    i = 0
    while (i < 10):
        loop()
        i = i + 1
    clean_up()
    

def setup():
    # Open Comms
    # Start WebUI
    # Load Config File
    

    # Backup Data Files
    DB.backup()

    # Initialize Data File
    pass

def loop():
    start = time.time()
    end = start + 1

    # Query Sensors
    #responses = {name:sensor.read_all() for (name, sensor) in SENSORS}
    #responses = {"gas pressure": SENSORS["gas pressure"].read_all(),
    #            "teros12": SENSORS["teros12"].read_all(),
    #            "oxygen": SENSORS["oxygen"].read_all(),
    #            "altitude": SENSORS["altitude"].read_all(),
    #            "pressure": SENSORS["pressure"].read_all(),
    #            "mass flow": SENSORS["mass flow"].read_all(),
    #            "co2": SENSORS["co2"].read_all(),

    #}

    #print(SENSORS)
    #responses = {"mass flow": SENSORS["mass flow"].read_all()}
    responses = {}
    for sensor in SENSORS:
        responses[sensor] = SENSORS[sensor].read_all()

    if (time.time() < end):
            print("Hit Target!")
    else:
        print("Missed Target! :(")

    # Record Data to File
    DB.log_data(responses)

    # Control Box (eg pump)

    pass

def clean_up():
    # Verify File Integrity?
    pass

if __name__ == "__main__":
    print("measure.py finished!")
