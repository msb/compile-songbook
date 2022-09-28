# Simple script that waits for a given file to be updated.
# TODO improve by not requiring that the file already exists.

# Set initial time of file
LTIME=`stat -c %Z $1`
ATIME=$LTIME

while [[ "$ATIME" == "$LTIME" ]]
do
  sleep 1
  ATIME=`stat -c %Z $1`
done
