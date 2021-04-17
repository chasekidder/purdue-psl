from configparser import ConfigParser
import os

class Config():
    def __init__(self, filename: str):
        self.FILE_NAME = filename
        self.parse(self.FILE_NAME)

    def refresh(self):
        self.parse(self.FILE_NAME)

    def parse(self, filename: str):
        parser = ConfigParser()

        parser.read(filename)

        self.PATH = os.path.dirname(__file__)
        self.WEBUI_PORT = parser.get("webui", "port")
        self.MEASURE_DURATION = parser.get("measurement", "duration")
        
        self.SENSORS_DIR = parser.get("sensor config", "directory")

        print(parser.items('sensors'))
        self.SENSORS = dict(parser.items('sensors'))

        #self.NANO_I2C_ADDR = int(parser.get("sensors", "nano_i2c_address"))
        # TEMPORARY: REMOVE LATER
        self.NANO_I2C_ADDR = 0x14


