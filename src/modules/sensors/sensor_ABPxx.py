from src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR
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

    def read_all(self) -> list:
        return [
            {
                "timestamp": time.time(),
                "type": "pressure",
                "value": self.read_pressure(),
                "unit": "psi",
            }
        ]

    def read_pressure(self) -> float:
        # ABPDANN060PGAA5 - ADS1115 ADC1
        # output (v) = ((0.8 * Vsupply)/(Pmax - Pmin)) * (Papplied - Pmin) + 0.10 * Vsupply
        # Vsupply = 5 volts
        # Pmax = 60 psi
        # Pmin = 0 psi
        
        Vout = self.adc.read_ADC1_V()
        return ((Vout - 0.5) * 60) / (4)


   