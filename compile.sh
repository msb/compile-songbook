#!/bin/bash

# wait for the html to pdf conversion to complete
/bin/bash /project/wait.sh ./html-to-pdf.done

echo compiling...

pushd download
chmod +x compile.sh
./compile.sh
popd

touch ./compile.done
