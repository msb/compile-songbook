#!/bin/sh

# wait for the `download` container to update `download.done` 
/bin/sh /project/wait.sh ./download.done

echo Templating title page...

cat download/00.title-page.html.template | sed -e "s/\${updated}/`date +"%d %B %Y"`/" > download/00.title-page.html

touch ./title-page.done
