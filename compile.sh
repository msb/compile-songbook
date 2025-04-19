#!/bin/bash

# wait for the html to pdf conversion to complete
/bin/bash /project/wait.sh ./html-to-pdf.done

echo compiling...

pdftk ./download/*.pdf cat output ./compiled.pdf
touch ./compile.done
