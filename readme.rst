========
kbdaemon
========


A small daemon utility that executes custom commands 
based on keystrokes captured from raw event device input.

This way you can bind pretty much every event,
normal keystrokes, media keys, joystick buttons or even your mouse buttons.


Installation
------------

I installed the required Python packages system-wide, 
because otherwise all executed applications 
are launched within the virtualenv, which I did not want.

  sudo pip(2) install evdev python-daemon


You can set up devices to use in ~/.kbdaemon.ini. Here is an example:


.. code-block:: ini

    [/dev/input/event2]
    192 = playerctl play-pause
    193 = playerctl next

    [/dev/input/event4]
    418 = xdotool key Page_Up
    419 = xdotool key Page_Down   


The number corresponds to the key id. 
You can look for key ids by running with --capture (see below)

Make sure you user has rights to access the device. 
On most systems, this can be done by adding your user to the 'input' group.


Usage
-----

Controlling the daemon:
  ./kbdaemon.py <start|stop>


Testing which events you want to capture (device is for instance event2, which maps to /dev/input/event2):
  ./kbdaemon.py --capture <device>


Notes
-----

Autostart seems to be a bit tricky at times, I got it working with the following command: 

  gnome-terminal -x sh ~/path/to/kbdeamon/start.sh


If you write a PKGBUILD for this, please let me know (so I can use it too ;)
