import logging
from robotInterface import *
from NPXconstants import *


class NPXCommand:
    def __init__(self, address, first_byte, body=None, name: str = None, is_request: bool = False):
        self.address = address
        self.first_byte = first_byte
        self.is_request = is_request
        if name is None:
            if is_request:
                self.name = "req: "
            else:
                self.name = "cmd: "
            self.name += hex(first_byte)
        else:
            self.name = name
        if body is None or not is_request:
            self.body = []
        else:
            self.body = body
            if name is None:
                self.name += " ["
                for b in body:
                    self.name += hex(b) + " "
                self.name += "]"


class CommandSpace:
    def __init__(self):
        self.commands = []

    def add_command(self, cmd: NPXCommand):
        self.commands.append(cmd)


class CommandMap:
    def __init__(self):
        self.storage = {}

    def put(self, http_cmd: str, rcpu_cmd: NPXCommand):
        self.storage[http_cmd] = rcpu_cmd

    def remove(self, http_cmd: str):
        for k in self.storage.keys():
            if k == http_cmd:
                del self.storage[http_cmd]


class CommandHandler:
    def __init__(self, command_map: CommandMap, robot_bus: RobotBus):
        self.map = command_map
        self.robot_bus = robot_bus

    def handle_command(self, http_command):
        found = False
        for k in self.map.storage:
            if k == http_command:
                logging.info("Got command: {}".format(http_command))
                found = True
                cmd = self.map.storage[k]
                if cmd.is_request:
                    return self.robot_bus.request(cmd.address, cmd.first_byte)
                else:
                    self.robot_bus.send(cmd.address, cmd.first_byte, cmd.body)
                    return "OK"
        if not found:
            logging.debug("Invalid command: {}".format(http_command))