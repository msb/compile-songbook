This application has been written very specifically to compile a songbook from other PDF sources for Cambridge Ukulele.
The application processes a set of index files referencing the source PDF, sorts and merges them into a single file.
It also creates a table of contents.

The application is containerised for portabilty. To build the container, run:

```bash
docker build -t compile-songbook .
```

Then, to run the application, run:

```bash
docker run --rm -u $(id -u):$(id -g) -v "$HOME/Documents/Songbooks:/data" compile-songbook cambridge-ukulele.pdf something-different.tsv old-cambridge-songbooks.tsv missing-wednesdays.tsv rob.tsv mikes-song-book.tsv
```

If you wish to run using the code on the host (eg, when developing), run:

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD:/app" -v "$HOME/Documents/Songbooks:/data" compile-songbook cambridge-ukulele.pdf something-different.tsv old-cambridge-songbooks.tsv missing-wednesdays.tsv rob.tsv mikes-song-book.tsv
```

