from src.modules.sensors.utils import Sensor, NANO, NANO_I2C_ADDR
import smbus2
import time

import re

class sensor(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

    def read_all(self) -> dict:

        return [
            {
                "timestamp": time.time(),
                "type": "oxygen partial pressure",
                "value": self.read_oxygen_partial_pressure(),
                "unit": "mbar",
            },
            {
                "timestamp": time.time(),
                "type": "oxygen concentration",
                "value": self.read_oxygen_percent(),
                "unit": "percent",
            },
            {
                "timestamp": time.time(),
                "type": "oxygen pressure",
                "value": self.read_oxygen_pressure(),
                "unit": "mbar",
            },
            {
                "timestamp": time.time(),
                "type": "oxygen temperature",
                "value": self.read_oxygen_temperature(),
                "unit": "celcius",
            },
        ]
       

    def read_oxygen_partial_pressure(self) -> float:
        command_string = "O\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
    

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        response = ''.join([chr(x) for x in value]).strip()
        resp_components = re.split("([O] \d*.\d*)", response)
        val = resp_components[1].split()[1]

        return val

    def read_oxygen_percent(self) -> float:
        command_string = "%\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
        print(value)

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        response = ''.join([chr(x) for x in value]).strip()
        resp_components = re.split("([%] \d*.\d*)", response)
        val = resp_components[1].split()[1]

        return val

    def read_oxygen_temperature(self) -> float:
        command_string = "T\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
        print(value)

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        response = ''.join([chr(x) for x in value]).strip()
        resp_components = re.split("([T] \d*.\d*)", response)
        val = resp_components[1].split()[1]

        return val

    def read_oxygen_pressure(self) -> float:
        target_time = time.time() + 0.25
        command_string = "P\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
            if(time.time() > target_time):
                return None
        print(value)

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        response = ''.join([chr(x) for x in value]).strip()
        resp_components = re.split("([P] \d*.\d*)", response)
        val = resp_components[1].split()[1]

        return val