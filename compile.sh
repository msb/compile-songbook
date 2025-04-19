#!/bin/bash

# wait for the `toc` container to update `toc.done` 
/bin/bash /project/wait.sh ./toc.done
echo compiling...
pdftk ./download/*.pdf cat output ./compiled.pdf
touch ./compile.done
