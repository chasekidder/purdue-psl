from src.modules.sensors.utils import Sensor
import time
from pa1010d import PA1010D

class GPS(Sensor):
    def __init__(self):
        self.gps = PA1010D()
    
    def read_all(self):
        result = self.gps.update()
        return self.gps.data




