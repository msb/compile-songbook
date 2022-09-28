# Songbook compilation

I maintain a number of different songbook PDFs the source of which are typically a file directory
containing a set of mostly single page PDFs for each song. The purpose of this project is to
orchestrate the compilation of these songbook PDFs by means of a `docker-compose` script.
The script runs 4 containers each concerned with different part of the process as follows:

- An [`rclone`](https://rclone.org/) container (`download`) synchronises the source PDF files from
  a remote folder to a docker volume.
- A [`python script`](https://github.com/msb/toc) (`toc`) that generates a set of TOC PDF files
  based on the file names of the local song files. Check the project's README for more details.
- A [`pdftk`](https://www.pdflabs.com/docs/pdftk-cli-examples/) container (`compile`) that compiles
  any title file, the TOC files and the song files into a single PDF.
- An [`rclone`](https://rclone.org/) container (`upload`) uploads the songbook to a remote folder.

Because there's no reliable way to make container dependent on each other, a `wait.sh` script is
used that simply waits on triggers files created in the volume by preceeding processes.

# Running the process

The process will require a couple of config files in the project folder. Firstly an env file must
be created with the following vars:

- BOOK_NAME (required): A slug that namespaces the files for a particular book in the `data`
  volume. TODO it would be nice to be able to namespace using the name of the env file.
- PAGES (required): The full `rclone` path of the remote source song files folder.
- BOOK (required): The full `rclone` path of the remote destination song book.
- TOC_COLS (optional): The max number of TOC rows
  (the default is defined in [`toc`](https://github.com/msb/toc))
- TOC_ROWS (optional): The max number of TOC columns
  (the default is defined in [`toc`](https://github.com/msb/toc))

The second config file is the `rclone.conf` file that must define the remote destination that will
be used to download the source song files and upload the compiled songbook. You can 
[run an interactive session to configure rclone](https://rclone.org/commands/rclone_config/) by
running:

```bash
docker run --name rclone_config -it rclone/rclone config
```

Once you have completed the session to can cn copy the file to the project folder:

```bash
docker cp rclone_config:/config/rclone/rclone.conf .
docker rm rclone_config
```

Now that you have defined you configuration to can run the process:

```bash
docker compose --env-file "my-song-book.env" up
```
