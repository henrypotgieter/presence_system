# Presence Sharing and Control System

![Presence Hardware](https://github.com/henrypotgieter/presence_system/blob/main/device.png?raw=true)

The purpose of this project is to enable a manually controlled presence
notification system.  Best used in a work from home environment where you have
a need to notify family members if you area available, busy or should not be
disturbed.  It also provides a time-tracking function so you can track how much
time you spend on different tasks.

For my purposes I want to track how much time I spend working at my normal job,
doing my own personal development work, other computer related learning
activities and my free time away from the desk.  I also want a way to easily
switch between the Free, Busy and DND modes displayed by my notifier system.

This is a simple setup that relies on the following components at the time of
building:

- Raspberry Pi 4 /w 4" LCD display (called ""notifier")
- Raspberry Pi 2B /w custom hat/PCB attached (called "punchclock")
- Telegraf on "punchclock" Pi
- InfluxDB and Grafana services to graph output gathered from punchclock Pi 
    telegraf instance

The 'hat' on the Raspberry Pi 2B I am using is a simple small breadboard stuck
on top of the case.  There are five momentary buttons that act as inputs, four
single color LED's (Red, Green, Blue and Yellow) as well as an RGB LED that
provide as outputs as well as some resistors and simple conductors to build the
circuit.  Not very pretty but functional.

![Circuit Up Close](https://github.com/henrypotgieter/presence_system/blob/main/closeup.png?raw=true)

# File locations for Punchclock Pi

The following files are located on the system in these locations, simply copy
them as you see fit:

```
punchclock.service  -   /etc/systemd/system/punchclock.service
punchclock.py       -   /usr/local/bin/punchclock.py
punchclock.sh       -   /usr/local/bin/punchclock.sh
punchstate.sh       -   /usr/local/bin/punchstate.sh
punchclock.conf     -   /etc/telegraf/telegraf.d/punchclock.conf
```

# Information about the notifier

The notifier system is very straight forward, you just need an RPi with a 4"
LCD display if you want this to look fancy, or you can use some other output
means.  Start off with a bare install of Raspbian.

- Install nginx/php-fpm on the pi:

```
$ sudo apt-get install -y nginx php-fpm
```

- Install inotify-tools, xdotool and xscreensaver:

```
$ sudo apt install -y inotify-tools xdotool xscreensaver
```

- Configure the X session screensaver to never start and to ensure the display
    does not turn off ever

- Write the following files to disk:

```
autostart       -   /etc/xdg/lxsession/LXDE-pi/autostart
start.sh        -   /usr/local/bin/start.sh
inotify.sh      -   /usr/local/bin/inotify.sh
index.php       -   /var/www/html/index.php
```

- Adjust your nginx config file to handle php via the php-fpm service, make
    sure to start and enable php-fpm and nginx

- Add the free, busy, and dnd images to your /home/pi/Pictures directory.
    These are green.jpg, yellow.jpg and red.jpg respectively.


Unless I missed something this will get you a working notifier host to interact
with.  When you visit the HTTP service on the Pi you'll see a simple web
interface that lets you adjust the status output as you see fit.  This should
also be the means by which the Punchclock device will control the output of the
display.

# Integrating with Grafana

I provided a sample of my dashboard I built as dashboard.json, so you can check
that out.  Here is what some sample output looks like:

![Grafana Dashboard](https://github.com/henrypotgieter/presence_system/blob/main/dashboard.png?raw=true)

# Code Provided As-Is

This isn't perfect code, but it suits my needs, feel free to modify as you see
fit if you want to adjust how any aspect works.
