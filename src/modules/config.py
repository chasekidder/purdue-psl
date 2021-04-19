from configparser import ConfigParser
import os

class Config():
    def __init__(self, file_name: str):
        self.FILE_NAME = file_name
        self.CWD = os.getcwd()
        self.PATH =  self.CWD + os.sep + "src" + os.sep

        self.parse(self.PATH + self.FILE_NAME)

    def refresh(self):
        self.parse(self.FILE_NAME)

    def parse(self, file_path: str):
        parser = ConfigParser()

        parser.read(file_path)

        self.WEBUI_PORT = parser.get("webui", "port")
        self.MEASURE_DURATION = parser.get("measurement", "duration")
        
        self.SENSORS_DIR = parser.get("sensor config", "directory")

        self.SENSORS = dict(parser.items('sensors'))

        #self.NANO_I2C_ADDR = int(parser.get("sensors", "nano_i2c_address"))
        # TEMPORARY: REMOVE LATER
        self.NANO_I2C_ADDR = 0x14


