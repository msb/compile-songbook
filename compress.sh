#!/bin/bash

touch ./compile.done
/project/wait.sh ./compile.done

echo compressing...
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=./compressed.pdf ./compiled.pdf

touch ./compress.publish.done
touch ./compress.upload.done
