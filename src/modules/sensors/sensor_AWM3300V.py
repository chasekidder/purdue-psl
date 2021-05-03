from src.modules.sensors.utils import Sensor, NANO_I2C_ADDR, NANO
from src.modules.sensors.ADS1115 import ADS1115
import smbus2
import time

class sensor(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        self.adc = ADS1115()

    def read_all(self) -> dict:
        return [
            {
                "timestamp": time.time(),
                "type": "mass flow", 
                "value": self.read_mass_flow(), 
                "unit": "sccm"
            }
        ]

    def read_mass_flow(self) -> float:
        # AWM3300V - ADS1115 ADC0
        # flow (sccm) ~~ (Vout / 2) * 1000
        # Vin = 5 volts
        # max = 1000

        Vout = self.adc.read_ADC0_V()
        return (Vout / 2.5) * 1000
