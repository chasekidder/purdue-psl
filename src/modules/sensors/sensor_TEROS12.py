from src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR
import smbus2
import time

import re


class sensor(Sensor):
    def __init__(self, address):
        self.address = address

        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

    def read_all(self) -> dict:
        response = self.read_sensor()
        response = ''.join([chr(x) for x in response])

        resp_components = re.findall("([+-][\d\.]+)", response)

        moisture = float(resp_components[0])
        temperature = float(resp_components[1])
        e_c = float(resp_components[2])
        

        return [
            {
                "timestamp": time.time(),
                "type": "temperature",
                "value": temperature,
                "unit": "celcius",
            },
            {
                "timestamp": time.time(),
                "type": "electrical conductivity",
                "value": e_c,
                "unit": "mS/cm",
            },
            {
                "timestamp": time.time(),
                "type": "volumetric water content",
                "value": moisture,
                "unit": "calibrated counts VWC",
            },
        ]


    def read_sensor(self) -> str:
        # Write TEROS-12 Command to the Nano's Command Register
        command_string = f"{ self.address }R0!"
        command_bytes = [ord(c) for c in command_string]
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 32)
            time.sleep(0.1)


        if (value[0] == 0x0F):
            print("0x0F response!")
            print(value)
            raise ValueError

        return value