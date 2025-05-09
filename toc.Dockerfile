FROM python:3.12-slim

WORKDIR /app

ADD ./toc/ ./

RUN apt update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # TODO maybe this could be dealt with using multi-stage builds
    pip install -r requirements.dev.txt

VOLUME /app
VOLUME /data

ENTRYPOINT ["/app/toc.py"]
