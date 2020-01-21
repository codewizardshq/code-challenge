FROM alpine:latest
LABEL maintainer="Sam Hoffman <sam@codewizardshq.com>"

ENV LANGUAGE=""
ENV CODEFILE=""

RUN apk --update add --no-cache python3 bash curl binutils libc-dev python3-dev gcc
RUN pip3 install -U pip
RUN pip3 install pyduktape

RUN adduser -D -H sandbox-user
USER sandbox-user

COPY "main.py" "/tmp/main.py"
VOLUME "/mnt/code"

ENTRYPOINT [ "/tmp/main.py" ]
