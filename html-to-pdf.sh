#!/bin/bash

# wait for both title page and table of contents
/bin/bash /project/wait.sh ./title-page.done ./toc.done

# convert all the html files to pdf files
for html in $(ls download/*.html); do
  echo converting $html to $html.pdf
  weasyprint $html $html.pdf
done

touch ./html-to-pdf.done
