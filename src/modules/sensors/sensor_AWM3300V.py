from psl_src.modules.sensors.utils import Sensor, NANO_I2C_ADDR, NANO
import smbus2
import time

class sensor(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

    def read_all(self) -> dict:
        return [
            {
                "timestamp": time.time(),
                "type": "mass flow", 
                "value": self.read_mass_flow(), 
                "unit": "asdf"
            }
        ]

    def read_mass_flow(self) -> float:
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A7, 2)
        
        value = value[1] << 8 | value[0]
        return value