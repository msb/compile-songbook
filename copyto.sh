#!/bin/sh

touch "$1"
# wait for the `compress` container to create the book
/bin/sh /project/wait.sh "$1"
echo copying to $2
# configure rclone
/project/rclone.conf.sh
# upload the book to a S3 bucket publically
rclone -v copyto "./compressed.pdf" "$2"
