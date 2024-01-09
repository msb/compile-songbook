#!/bin/sh

BOOK=./compiled.pdf
touch "$BOOK"
# wait for the `compile` container to create the book 
# (we rely on a different flag to `publish` because they can interfere)
/bin/sh /project/wait.sh "$BOOK"
echo uploading...
# configure rclone
/project/rclone.conf.sh
# upload the book to the remote folder
rclone -v copyto "$BOOK" "$1"
