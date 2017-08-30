#!/bin/bash

which youtube-dl
RET=$?

if [[ ${RET} != 0 ]]; then
	echo "Error: couldn't find the youtube-dl utility."
	echo "On apt-get systems: apt-get install youtube-dl"
	echo "On yum systems: yum install youtube-dl"
	echo ""
	echo "You can also download it from github:"
	echo "https://rg3.github.io/youtube-dl/"
fi


mkdir -p videos
cd videos

for i in `cat ../video_ids.txt`; do
	if [[ ! -f "${i}.mp4" ]]; then
		echo "Downloading ${i}"
		youtube-dl -f mp4 "http://www.youtube.com/watch?v=${i}" --output "${i}.mp4"
		sleep 2
	else
		echo "SKIPPING ${i}"
	fi
done
