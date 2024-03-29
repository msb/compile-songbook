#!/bin/sh

if [[ -z $1 ]] ; then
    echo nothing to publish
    exit 0
fi

touch ./compile.done
# wait for the `compile` container to create the book
# (we rely on a different flag to `upload` because they can interfere)
/bin/sh /project/wait.sh ./compile.done
echo publishing...
# configure rclone
/project/rclone.conf.sh
# upload the book to a S3 bucket publically
rclone copyto "./compiled.pdf" "$1"
