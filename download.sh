#!/bin/sh

echo downloading...
# configure rclone
/project/rclone.conf.sh
# synchronises the remore PDF song files to the docker volume
rclone -v sync "$1" ./download
touch ./download.done
