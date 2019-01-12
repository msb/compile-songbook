FROM python:3.7-alpine

WORKDIR /data

RUN apk add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf ttf-opensans

RUN pip install PyPDF2 docopt WeasyPrint

ADD ./compile-songbook.py /app/

# can be overridden for development
VOLUME /app

VOLUME /data

ENTRYPOINT ["python3", "/app/compile-songbook.py"]

CMD []

