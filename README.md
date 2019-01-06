```bash
docker build -t compile-songbook .
```

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD:/app" -v "$HOME/Documents/Songbooks:/data" compile-songbook CambridgeUkulele.pdf something-different.tsv old-cambridge-songbooks.tsv missing-wednesdays.tsv rob.tsv mikes-song-book.tsv
```

