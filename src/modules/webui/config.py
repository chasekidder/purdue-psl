import os

class BaseConfiguration():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SECRET_KEY = "f62c0c78db951fcc952e6b534e82d35e16e95136c64f4f31"
    DATA_FOLDER = "/media/usb0/"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfiguration(BaseConfiguration):
    DEBUG = True

class TestConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfigurateion(BaseConfiguration):
    pass