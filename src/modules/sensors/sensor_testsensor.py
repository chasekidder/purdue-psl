from src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR

import time
import random

class sensor(Sensor):
    def __init__(self):
        time.sleep(0.01)

    def read_all(self) -> list:
        return [
            {
                "timestamp": time.time(),
                "type": "test_type",
                "value": self.read_test_data(),
                "unit": "test_unit",
            }
        ]

    def read_test_data(self) -> float:
        value = random.randint(0, 100)

        return value