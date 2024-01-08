# Songbook compilation

I maintain a number of different songbook PDFs the source of which are typically folder with
set of mostly single page PDFs for each song. The purpose of this project is to
orchestrate the compilation of these songbook PDFs by means of a `docker-compose` script.
The script runs 5 containers each concerned with different parts of the process as follows:

- An [`rclone`](https://rclone.org/) container (`download`) synchronises the source PDF files from
  a remote folder to a docker volume.
- A [`python script`](https://github.com/msb/toc) (`toc`) generates a set of TOC PDF files
  based on the file names of the local song files. Check the project's README for more details.
- A [`pdftk`](https://www.pdflabs.com/docs/pdftk-cli-examples/) container (`compile`) compiles
  any title file, the TOC files and the song files into a single PDF.
- An [`rclone`](https://rclone.org/) container (`upload`) uploads the songbook to a remote folder.
- Optionally an [`s3cmd`](https://github.com/s3tools/s3cmd) container (`publish`) publishes the songbook to an S3 url.

Because there's no reliable way to make containers dependent on each other, a `wait.sh` script is
used that simply waits on trigger files created in the volume by preceding processes.

# Running the process

The process will require a couple of config files in the project folder. Firstly an env file must
be created with the following vars:

- `BOOK_NAME` (required): A slug that namespaces the files for a particular book in the `data`
  volume. TODO it would be nice to be able to namespace using the name of the env file itself.
- `PAGES` (required): The full `rclone` path of the remote source song files folder.
- `BOOK` (required): The full `rclone` path of the remote destination song book.
- `TOC_COLS` (optional): The max number of TOC rows
  (the default is defined in [`toc`](https://github.com/msb/toc/blob/main/toc.py))
- `TOC_ROWS` (optional): The max number of TOC columns
  (the default is defined in [`toc`](https://github.com/msb/toc/blob/main/toc.py))
- `PUBLISHING_TO` (optional): An S3 url that, if defined, is used to publish the book to.

The second config file is the `rclone.conf` file that must define the remote destination that will
be used to download the source song files and upload the compiled songbook. You can 
[run an interactive session to configure rclone](https://rclone.org/commands/rclone_config/) by
running:

```bash
docker run --name rclone_config -it rclone/rclone config
```

Once you have completed the session to can copy the file to the project folder:

```bash
docker cp rclone_config:/config/rclone/rclone.conf .
docker rm rclone_config
```

If you are also publishing the book to an S3 bucket then you also need an `.s3cfg` file in the
project root (to provide the S3 credentials as a minimum). You can run an interactive session to
configure s3cmd by running:

```bash
# TODO: this doesn't actually work very well as the input prompts don't work correctly.
# You're probably better off making the `.s3cfg` by some other means.
docker run --name s3cmd_config -it schickling/s3cmd --configure
```

Once you have completed the session to can copy the file to the project folder:

```bash
docker cp s3cmd_config:/root/.s3cfg .
docker rm s3cmd_config
```

Now that you have defined the configuration to can run the process:

```bash
docker compose --env-file "my-song-book.env" up
```
