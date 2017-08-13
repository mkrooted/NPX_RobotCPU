from flask import Flask
from robotInterface import *
from commandHandler import *
from NPXconstants import *
import logging

logging.basicConfig(level=logging.DEBUG)
logging.info("Let the debug begin!")

# Prerequisites
NPXBus = RobotBus()
NPXBus.scan_modules()

# Configuring command space
command_map = CommandMap()
command_map.put("led_on", NPXCommand(0x41, 0xfa, [0xaa]))
command_map.put("led_off", NPXCommand(0x41, 0xfb))
command_map.put("status", NPXCommand(0x41, 0xf0, is_request=True))

# Configuring command handler
command_handler = CommandHandler(command_map, NPXBus)

# Setting up web server
app = Flask(__name__)


@app.route('/cmd/<cmd>')
def test_cmd(cmd):
    data = command_handler.handle_command(cmd)
    return str(data)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
