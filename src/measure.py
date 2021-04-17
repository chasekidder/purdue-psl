from .modules import database
from .modules.config import Config

from .modules.sensors import NANO

from .modules.ui.celery import task_queue
#celery = Celery(broker="redis://localhost:6379/0")


import time
from psl_src.modules.sensors import init_sensor


CONFIG = Config("config.ini")

DB = database.Database()

# Initialize Sensors

SENSORS = {
    "gas pressure": init_sensor(CONFIG.SENSORS["Mass Flow 1"]),

}

@task_queue.task(name="measurement.cycle")
def measurement_cycle():
    setup()
    i = 0
    while (i < 1):
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
    responses = {"gas pressure": SENSORS["gas pressure"].read_all(),
                "teros12": SENSORS["teros12"].read_all(),
                "oxygen": SENSORS["oxygen"].read_all(),
                "altitude": SENSORS["altitude"].read_all(),
                "pressure": SENSORS["pressure"].read_all(),
                "mass flow": SENSORS["mass flow"].read_all(),
                "co2": SENSORS["co2"].read_all(),

    }

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
    print("dont run me!")
    print(SENSORS)