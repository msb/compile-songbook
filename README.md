This application has been written very specifically to compile a songbook from other PDF sources
for Cambridge Ukulele. The application processes a set of index files referencing the source PDF,
sorts and merges them into a single file. It also creates a table of contents and an optional 
title.

The application is containerised for portabilty. To build the container, run:

```bash
docker build -t compile-songbook .
```

Then, to run the application, run:

```bash
./compile-songbook.sh
```

If you wish to run using the code on the host (eg, when developing), run as required:

```bash
docker run compile-songbook --help

docker run -v "$PWD:/app" -v "$HOME/Documents/Songbooks:/data" --rm \
-u $(id -u):$(id -g) compile-songbook ...
```
