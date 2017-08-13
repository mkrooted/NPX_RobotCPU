import logging
import smbus
from NPXconstants import *


class NPXModule:
    def __init__(self, address, info=None):
        self.address = address
        self.info = info


class RobotBus:
    def __init__(self):
        self.bus = smbus.SMBus(BUS_ID)
        self.modules = []
        self.module_counter = 0

    def add_module(self, npx_module: NPXModule):
        logging.info("New module on 0x{}".format(hex(npx_module.address)))
        self.modules.append(npx_module)
        self.module_counter += 1

    def scan_modules(self):
        logging.debug("Scanning I2C bus...")
        for addr in range(MIN_I2C_ADDR, MAX_I2C_ADDR):
            try:
                self.bus.read_byte(addr)
                logging.debug("Found module #{} on {}".format(self.module_counter, hex(addr)))
            except:
                pass
        logging.debug("I2C Scan finished")

    def send(self, address, first_byte, body_bytes: list):
        logging.info("Sending {} to 0x{}".format(hex(first_byte) + " [" + " ".join(body_bytes) + "]", hex(address)))
        self.bus.write_i2c_block_data(address, first_byte, body_bytes)

    def request(self, address, first_byte):
        logging.info("Requesting {} from 0x{}".format(hex(first_byte), hex(address)))
        data = self.bus.read_byte_data(address, first_byte)
        logging.debug("RES TO {}: {}".format(hex(first_byte), data))
        return data
