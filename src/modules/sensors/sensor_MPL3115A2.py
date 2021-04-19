from src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR, try_io
import smbus2
import time


class sensor(Sensor):
    I2C_ADDRESS = 0x60
    REGISTER_STATUS_ADDRESS = 0x00
    REGISTER_PRESSURE_MSB = 0x01
    REGISTER_ALTITUDE_MSB = 0x01
    REGISTER_TEMP_MSB = 0x04
    BAR_IN_MSB = 0x14

    class CTRL_REG1:
        ADDRESS = 0x26
        SBYB = 0x01
        OST = 0x02
        RST = 0x04
        OS0 = 0x08
        OS1 = 0x10
        OS2 = 0x20
        RAW = 0x40
        ALT = 0x80

    class PT_DATA_CFG:
        ADDRESS = 0x13
        TDEFE = 0x01
        PDEFE = 0x02
        DREM = 0x04

    def __init__(self):
        address = MPL3115A2.I2C_ADDRESS

        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # 0x07 (7) Enable data ready events Altitude, Pressure, Temperature
        byteVal = MPL3115A2.PT_DATA_CFG.TDEFE | MPL3115A2.PT_DATA_CFG.PDEFE | MPL3115A2.PT_DATA_CFG.DREM
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.PT_DATA_CFG.ADDRESS, byteVal)

    def read_all(self) -> dict:
        kpa = try_io(lambda: self.read_pressure())

        return [
            {
                "timestamp": time.time(),
                "type": "barometric pressure",
                "value": kpa,
                "unit": "kpa",
            },
            {
                "timestamp": time.time(),
                "type": "altitude",
                "value": (44330.77 * (1 - pow(((kpa * 1000) / 101326), (0.1902632)))),
                "unit": "meters",
            },
            {
                "timestamp": time.time(),
                "type": "temperature",
                "value": self.read_temperature_c(),
                "unit": "celcius",
            },
        ]


    def read_pressure(self) -> float:
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read barometric pressure (3 bytes)
        # Pressure MSB, Pressure CSB, Pressure LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_PRESSURE_MSB, 3)

        # Convert to 20-bit integer
        pressure_pa = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 4.0
        pressure_kpa = pressure_pa / 1000.0

        return pressure_kpa

    def read_altitude(self) -> float:
        # 0xB9 (185) Active Mode, OSR = 128, Altimeter Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB | MPL3115A2.CTRL_REG1.ALT
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read altitude (3 bytes)
        # Altitude MSB, Altitude CSB, Altitude LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_ALTITUDE_MSB, 3)

        # Convert to 20-bit integer
        altitude = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 16.0

        return altitude

    def read_temperature_c(self) -> float:
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read ambiant temperature (2 bytes)
        # Temperature MSB, Temperature LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_TEMP_MSB, 2)

        # Convert to 20-bit integer
        altitude = (((data[0]<<8) + (data[1] & 0xF0)) / 16) / 16.0

        return altitude

    def read_temperature_f(self) -> float:
        temp_c = self.read_temperature_c()
        temp_f = (temp_c * 1.8) + 32

        return temp_f

    def calibrate_sea_level(self, pascal:float = 101326):
        if ((pascal / 2) > 65535):
            raise ValueError("Calibration Number Too Large")

        bar_hg = pascal / 2
        data = [int(bar_hg) >> 8, int(bar_hg) & 0xF0 ]
        self.bus.write_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.BAR_IN_MSB, data)