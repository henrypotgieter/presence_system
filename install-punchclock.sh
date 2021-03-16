#!/bin/bash
# Very simple install script for punchclock element

if [[ $UID -ne 0 ]] ; then
    echo "Run me as root!"
    exit 1
fi

cp punchclock/punchclock.service /etc/systemd/system/punchclock.service
cp punchclock/punchclock.py /usr/local/bin/punchclock.py
cp punchclock/punchclock.sh /usr/local/bin/punchclock.sh
cp punchclock/punchstate.sh /usr/local/bin/punchstate.sh

if [ -d "/etc/telegraf/telegraf.d" ] ; then
    cp punchclock/punchclock.conf /etc/telegraf/telegraf.d/punchclock.conf
fi

chmod a+x /usr/local/bin/punchclock.sh
chmod a+x /usr/local/bin/punchstate.sh

touch /var/punchclock.led.state
touch /var/punchclock.dnd.state

systemctl daemon-reload
systemctl enable punchclock
systemctl start punchclock
