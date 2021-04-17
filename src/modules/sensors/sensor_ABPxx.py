from psl_src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR

import smbus2
import time

class ABPxx(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

    def read_all(self) -> list:
        return [
            {
                "timestamp": time.time(),
                "type": "pressure",
                "value": self.read_pressure(),
                "unit": "mbar",
            }
        ]

    def read_pressure(self) -> float:
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A2, 2)
        
        value = value[1] << 8 | value[0]

        return value