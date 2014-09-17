========
kbdaemon
========


A small daemon utility that executes custom commands based on keystrokes not detected by the system.

Installation
------------

I installed the required Python packages system-wide, because otherwise all executed applications 
are launched within the virtualenv, which I did not want.

  sudo pip(2) install evdev python-daemon


You can set up a device to use in ~/.kbdaemon.ini. Use the provided example .kbdaemon.ini as a base, copy it first.

Make sure you user has rights to access the device. On most systems, this can be done by adding your user to the 'input' group.


Usage
-----

  ./kbdaemon.py --capture <device> (test which events you want to capture)
                                   (device is for instance event2, which maps to /dev/input/event2)

  ./kbdaemon.py <start|stop>       (control the daemon)



Notes
-----

This currently only supports one device, until it's rewritten with asyncore.

Autostart seems to be a bit tricky at times, I got it working with the following command: 'gnome-terminal -x sh ~/path/to/kbdeamon/start.sh'
