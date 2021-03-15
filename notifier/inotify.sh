#!/bin/sh
export DISPLAY=:0.0
while inotifywait -e modify,create,delete /usr/share/rpd-wallpaper/temple.jpg
do
	pcmanfm --display=:0.0 --wallpaper-mode=color ; pcmanfm --display=:0.0 --wallpaper-mode=stretch
done
