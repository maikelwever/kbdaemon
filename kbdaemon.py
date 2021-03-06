#!/usr/bin/env python2

# NOTE: Install the Python evdev package first: sudo pip install evdev
# NOTE: Install the Python daemon package also: sudo pip install python-daemon

from daemon import runner
from os.path import abspath, exists, expanduser
from os import system
from select import select

import ConfigParser
import evdev
import sys


CONFIG_FILE = abspath(expanduser("~/.kbdaemon.ini"))


class App():
    def __init__(self):
        self.stdin_path = "/dev/null"
        self.stdout_path = "/dev/null"
        self.stderr_path = "/dev/null"
        self.pidfile_path = '/tmp/kbdaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        self.main()

    def debug(self, device):
        dev = evdev.InputDevice("/dev/input/{}".format(device))
        print("Device chosen:")
        print(dev)

        for event in dev.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.value == evdev.KeyEvent.key_hold or event.value == evdev.KeyEvent.key_down:
                    print(evdev.categorize(event))

    def main(self):
        parser = ConfigParser.RawConfigParser()
        parser.read(CONFIG_FILE)

        devices = {}

        for section in parser.sections():
            if not exists(section):
                raise Exception("Given device {} does not exist (or is not accessible)!".format(section))

            devices[section] = dict(parser.items(section))
            """
            if 'exclusive' in commands:
                if int(commands['exclusive']):
                    exclusive = True
                del commands['exclusive']
            """

        for device in devices.keys():
            print("Binding to device: {}".format(device))

        input_devices = map(evdev.InputDevice, devices.keys())
        input_devices = {dev.fd: dev for dev in input_devices}

        while True:
            r, w, x = select(input_devices, [], [])
            for fd in r:
                device = input_devices[fd]
                for event in device.read():
                    print(event)
                    if event.type == evdev.ecodes.EV_KEY:
                        if event.value == evdev.KeyEvent.key_hold or \
                                event.value == evdev.KeyEvent.key_down:

                            if str(event.code) in devices[device.fn]:
                                cmd = devices[device.fn][str(event.code)]
                                print("Executing {0}".format(cmd))
                                system('nohup sh -c "(cd ~ && {0})" & disown'.format(cmd))


if __name__ == "__main__":
    app = App()
    if len(sys.argv) > 1 and sys.argv[1] == "--capture":
        app.debug(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--debug":
        app.main()
    else:
        daemon_runner = runner.DaemonRunner(app)
        daemon_runner.do_action()
