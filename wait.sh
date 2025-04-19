# Script that waits for each file given as an argument to be updated (touched).
# If the file doesn't exist, it will be created.

# For each file given as an argument, ..
for done in "$@"
do
  # .. ensure it exists ..
  touch "$done"
  # .. and save the file's timestamp in a var named with a slug of the filename.
  slug=$(echo "$done" | sed -E 's/[^a-zA-Z0-9]+/_/g')
  eval initial_ts$slug=`stat -c %Z $done`
done

all_touched=false

# While any of the file's haven't been touched, ..
while [[ $all_touched == false ]]
do
  # .. wait for a second .. 
  sleep 1
  # .. and then test each file to see if it's timestamp has changed.
  # We do this by assuming all of them have been touched and then searching
  # for a single contradictory case.
  all_touched=true
  for done in "$@"
  do
    # 
    slug=$(echo "$done" | sed -E 's/[^a-zA-Z0-9]+/_/g')
    initial_ts=$(eval echo \$initial_ts$slug)
    timestamp=`stat -c %Z $done`
    if [[ "$timestamp" == "$initial_ts" ]]; then
      all_touched=false
      break
    fi
  done
done
