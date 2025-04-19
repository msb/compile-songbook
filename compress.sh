#!/bin/sh

/project/wait.sh ./compile.done

echo compressing...
pdfsizeopt ./compiled.pdf ./compressed.pdf

touch ./compress.publish.done
touch ./compress.upload.done
