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

    def read_all(self) -> dict:
        return [
            {
                "timestamp": time.time(),
                "type": "co2 1", 
                "value": self.read_co2_concentration_0(), 
                "unit": "ppm"
            },
            {
                "timestamp": time.time(),
                "type": "co2 2", 
                "value": self.read_co2_concentration_1(), 
                "unit": "ppm"
            }
        ]

    def read_co2_concentration_0(self) -> float:
        # GMP251 - ADS1115 ADC2
        # concentration (ppm) = (Vout / Vin) * Cmax
        # Vin = 5 volts
        # Cmax = 200000 ppm

        Vout = self.adc.read_ADC2_V()
        return (Vout / 5) * 200000

    def read_co2_concentration_1(self) -> float:
        # GMP251 - ADS1115 ADC3
        # concentration (ppm) = (Vout / Vin) * Cmax
        # Vin = 5 volts
        # Cmax = 200000 ppm

        Vout = self.adc.read_ADC3_V()
        return (Vout / 5) * 200000