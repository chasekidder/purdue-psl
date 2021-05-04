import os
import random
import datetime
import re

from src.measure import SENSORS
from src.modules.database import DB


def get_files_in_dir(path:str) -> list:
    return os.listdir(path)


def old_get_live_data():
    return {
            "timestamp": datetime.datetime.now(),
            "Electrical Conductivity": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Moisture": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Temperature": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Carbon Dioxide": random.randint(1,10),
            "Oxygen": random.randint(1,10),
            "Gas Pressure": random.randint(1,10)
            }

def get_live_data():
    # data = {}

    # for sensor in SENSORS:
    #     data[sensor] = DB.get_most_recent(sensor)

    return DB.get_most_recent()

def get_site_list():
    site_list = []

    sites = DB.get_site_list()
    for site in sites:
        site_list.append(f"""ID: {site["id"]}   Name: {site["name"]}    Depth: {site["depth"]}  Lat: {site["latitude"]} Long: {site["longitude"]}""")

    return site_list


def str_to_bytes(data: str) -> bytes:
    return data.encode()

def bytes_to_str(data: bytes, encoding: str="utf-8") -> str:
    return data.decode(encoding)

def parse_regex(data: str, pattern: str) -> list:
    return re.split(pattern, data)