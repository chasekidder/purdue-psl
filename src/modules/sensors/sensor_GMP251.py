from psl_src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR
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
                "type": "co2 concentration", 
                "value": self.read_co2_concentration(), 
                "unit": "percent"
            }
        ]

    def read_co2_concentration(self) -> float:
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A2, 2)
        
        value = (((value[1] << 8 | value[0]) / 1024) * 200000)
        
        return value