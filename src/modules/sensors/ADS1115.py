from src.modules.sensors.utils import Sensor
import smbus2
import time


class ADS1115(Sensor):
    # 0x48 (1001 000) (ADDR = GND)
    I2C_ADDRESS = 0x48 

    CONV_REG_ADDR = 0x00
    CONF_REG_ADDR = 0x01
    LOW_THRESHOLD_REG_ADDR = 0x02
    HIGH_THRESHOLD_REG_ADDR = 0x03

    class CONF_REG:
        ADDRESS = 0x01

        COMP_QUE0 = 0x0001
        COMP_QUE1 = 0x0002
        COMP_LAT = 0x0004
        COMP_POL = 0x0008
        COMP_MODE = 0x0010
        DR0 = 0x0020
        DR1 = 0x0040
        DR2 = 0x0080

        MODE = 0x0100
        PGA0 = 0x0200
        PGA1 = 0x0400
        PGA2 = 0x0800
        MUX0 = 0x1000
        MUX1 = 0x2000
        MUX2 = 0x4000
        OS = 0x8000

    # Convenience Values
    ADC0 = CONF_REG.MUX2
    ADC1 = CONF_REG.MUX2 | CONF_REG.MUX0
    ADC2 = CONF_REG.MUX2 | CONF_REG.MUX1
    ADC3 = CONF_REG.MUX2 | CONF_REG.MUX1 | CONF_REG. MUX0

    DEFAULTS = CONF_REG.MODE | CONF_REG.DR2 | CONF_REG.COMP_QUE1 | CONF_REG.COMP_QUE1


    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        # Reset to default settings
        byteVal = ADS1115.DEFAULTS

        self.bus.write_byte_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG.ADDRESS, byteVal)
        time.sleep(.001)

    def read_all(self) -> list:
        return [
            {
                "timestamp": time.time(),
                "type": "voltage",
                "value": self.read_ADC0(),
                "unit": "volts",
            },
            {
                "timestamp": time.time(),
                "type": "voltage",
                "value": self.read_ADC1(),
                "unit": "volts",
            },
            {
                "timestamp": time.time(),
                "type": "voltage",
                "value": self.read_ADC2(),
                "unit": "volts",
            },
            {
                "timestamp": time.time(),
                "type": "voltage",
                "value": self.read_ADC3(),
                "unit": "volts",
            }
        ]

    def read_ADC0(self) -> int:
        byteVal = ADS1115.DEFAULTS | ADS1115.ADC0 | ADS1115.CONF_REG.OS
        self.bus.write_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, [(byteVal >> 8) & 0xFF, byteVal & 0xFF])
        time.sleep(.001)
        return self.read_conversion()

    def read_ADC1(self) -> int:
        byteVal = ADS1115.DEFAULTS | ADS1115.ADC1 | ADS1115.CONF_REG.OS
        self.bus.write_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, [(byteVal >> 8) & 0xFF, byteVal & 0xFF])
        time.sleep(.001)
        return self.read_conversion()

    def read_ADC2(self) -> int:
        byteVal = ADS1115.DEFAULTS | ADS1115.ADC2 | ADS1115.CONF_REG.OS
        self.bus.write_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, [(byteVal >> 8) & 0xFF, byteVal & 0xFF])
        time.sleep(.001)
        return self.read_conversion()

    def read_ADC3(self) -> int:
        byteVal = ADS1115.DEFAULTS | ADS1115.ADC3 | ADS1115.CONF_REG.OS
        self.bus.write_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, [(byteVal >> 8) & 0xFF, byteVal & 0xFF])
        time.sleep(.001)
        return self.read_conversion()

    def read_ADC0_V(self) -> float:
        fullRange = 6.144
        bitResolution = 32768
        return (self.read_ADC0() * (fullRange / bitResolution))

    def read_ADC1_V(self) -> float:
        fullRange = 6.144
        bitResolution = 32768
        return (self.read_ADC1() * (fullRange / bitResolution))

    def read_ADC2_V(self) -> float:
        fullRange = 6.144
        bitResolution = 32768
        return (self.read_ADC2() * (fullRange / bitResolution))

    def read_ADC3_V(self) -> float:
        fullRange = 6.144
        bitResolution = 32768
        return (self.read_ADC3() * (fullRange / bitResolution))

    def read_conversion(self) -> float:
        # Wait for conversion bit to signal a completed sample
        value = self.bus.read_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, 2)
        time.sleep(.001)
        while ((value[1] & ADS1115.CONF_REG.OS) != 0):
            value = self.bus.read_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONF_REG_ADDR, 2)
            time.sleep(.001)

        # Read conversion result
        value = self.bus.read_i2c_block_data(ADS1115.I2C_ADDRESS, ADS1115.CONV_REG_ADDR, 2)
        return value[0] << 8 | value[1]