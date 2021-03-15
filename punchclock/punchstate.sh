#!/bin/bash
# State check script to be called by telegraf

state=$(cat /var/punchclock.led.state)
dndstate=$(cat /var/punchclock.dnd.state)
hostname=`hostname`

red=0
green=0
blue=0
yellow=0
dnd=0

if [[ $state == "red" ]] ; then
	red=1
elif [[ $state == "green" ]] ; then
	green=1
elif [[ $state == "blue" ]] ; then
	blue=1
elif [[ $state == "yellow" ]] ; then
	yellow=1
fi
if [[ $dndstate == "yes" ]] ; then
	dnd=1
fi

echo -n "work_status,host=$hostname red=$red,green=$green,blue=$blue,yellow=$yellow,dnd=$dnd"
