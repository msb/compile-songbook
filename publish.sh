#!/bin/sh

if [[ -z $1 ]] ; then
    echo nothing to publish
    exit 0
fi

BOOK=./compiled.pdf
touch "$BOOK"
# wait for the `compile` container to create the book 
/bin/sh /project/wait.sh "$BOOK"
echo publishing...
# upload the book to a S3 bucket publically
s3cmd --config=/project/.s3cfg put "$BOOK" "$1" --acl-public
