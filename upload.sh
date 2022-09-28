#!/bin/sh

BOOK=./compiled.pdf
touch "$BOOK"
# wait for the `compile` container to create the book 
/bin/sh /project/wait.sh "$BOOK"
echo uploading...
mkdir -p /config/rclone
# Copying the host's `rclone.conf` file works better as `rclone` attempts to write it's own config
# file to `/project` and fails as it is RO.
cp /project/rclone.conf /config/rclone/
# upload the book to the remote folder
rclone -v copyto "$BOOK" "$1"
