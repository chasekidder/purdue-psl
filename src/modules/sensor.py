import importlib
import importlib.util

import os

from src.modules.config import Config

# Import all sensor submodules
from os.path import dirname, basename, isfile, join
import glob
import importlib.util

CONFIG = Config("config.ini")

SENSOR_MODULES = []
sensors_path = CONFIG.PATH + "modules" + os.sep + "sensors" + os.sep

modules = glob.glob(join(dirname(sensors_path), "*.py"))
for f in modules:
    if isfile(f) and not f.endswith("__init__.py"):
        module_name = basename(f[:-3])

        spec = importlib.util.spec_from_file_location(module_name, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        SENSOR_MODULES.append(mod)
        
        

        

def init_sensor(sensor_name):
    for module in SENSOR_MODULES:
        #print(module.__name__)
        if sensor_name in module.__name__:
            return module.sensor()

    return None








