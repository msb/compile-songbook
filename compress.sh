#!/bin/sh

# TODO provide sed in the compress image so we can remove the need for `simple-wait.sh`
/project/simple-wait.sh ./compile.done

echo compressing...
pdfsizeopt --quiet ./compiled.pdf ./compressed.pdf

touch ./compress.publish.done
touch ./compress.upload.done
