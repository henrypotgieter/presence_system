#!/bin/bash
# Very simple install script for punchclock element

# Check if we're running as root (so we can copy things) or inform the user otherwise
if [[ $UID -ne 0 ]] ; then
    echo "Run me as root!"
    exit 1
fi

# Copy files to where they need to go
cp punchclock/punchclock.service /etc/systemd/system/punchclock.service
cp punchclock/punchclock.py /usr/local/bin/punchclock.py
cp punchclock/punchclock.sh /usr/local/bin/punchclock.sh
cp punchclock/punchstate.sh /usr/local/bin/punchstate.sh

# Check if there's a telegraf config directory and if so add the telegraf config
if [ -d "/etc/telegraf/telegraf.d" ] ; then
    cp punchclock/punchclock.conf /etc/telegraf/telegraf.d/punchclock.conf
fi

# Rewrite the IP for the notifier host
echo -n "Enter the IP of your notifier host for PunchClock to interface with: "
read notifier
sed -i "/NOTIFIER_IP = /c\NOTIFIER_IP = \"$notifier\"" /usr/local/bin/punchclock.py

# Make sure shell scripts can execute
chmod a+x /usr/local/bin/punchclock.sh
chmod a+x /usr/local/bin/punchstate.sh

# Touch the var files we'll use to track state
touch /var/punchclock.led.state
touch /var/punchclock.dnd.state

# Enable and start that daemon
systemctl daemon-reload
systemctl enable punchclock
systemctl start punchclock
