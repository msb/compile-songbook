#!/bin/sh

mkdir -p /config/rclone
# Copying the host's `rclone.conf` file works better as `rclone` attempts to write it's own config
# file to `/project` and fails as it is RO.
cp /project/rclone.conf /config/rclone/
