from psl_src.modules.config import Config

CONFIG = Config("config.ini")

class Sensor():
    def __init__(self):
        pass
        
    def read_all(self):
        raise NotImplementedError

    def calibrate(self):
        raise NotImplementedError

# Arduino Nano I2C Address
NANO_I2C_ADDR = CONFIG.NANO_I2C_ADDR

# Arduino Nano I2C Command Registers
class NANO():
    CMD_REG_WRITE = 0x00

    A_READ_A0 = 0x10 
    A_READ_A1 = 0x11
    A_READ_A2 = 0x12 # ABPxx Pressure Sensor
    A_READ_A3 = 0x13 # GMP 251 CO2 Sensor
    A_READ_A4 = 0x14 # I2C SCL
    A_READ_A5 = 0x15 # I2C SDA
    A_READ_A6 = 0x16 
    A_READ_A7 = 0x17 # AWM3300V Mass Flow Sensor

    SDI12_READ = 0x20
    SDI12_POLL = 0x21

    UART0_READ = 0x30
    UART1_READ = 0x31

    UART0_POLL = 0x32
    UART1_INIT = 0x33

    PUMP_CTRL_REG = 0x50


def try_io(call, tries=10):
    assert tries > 0
    error = None
    result = None

    while tries:
        try:
            result = call()
        except IOError as e:
            error = e
            tries -= 1
        else:
            break

    if not tries:
        raise error

    return result
