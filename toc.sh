#!/bin/bash

# wait for the `download` container to update `download.done` 
/bin/bash /project/wait.sh ./download.done
echo creating TOC...
cols_opt=$([ -z "$TOC_COLS" ] && echo "" || echo "--toc-cols=$TOC_COLS")
rows_opt=$([ -z "$TOC_ROWS" ] && echo "" || echo "--toc-rows=$TOC_ROWS")
/app/toc.py ./download $cols_opt $rows_opt
touch ./toc.done
