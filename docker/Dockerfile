FROM alpine:latest
LABEL maintainer="Sam Hoffman <sam@codewizardshq.com>"

RUN apk --update add --no-cache python3 bash curl binutils libc-dev python3-dev gcc
RUN pip3 install -U pip
RUN pip3 install flask flask-cors pyduktape gunicorn

RUN adduser -D -H webapp
RUN mkdir -p "/var/www/flaskapp"

# default Flask port
EXPOSE 5000/tcp

USER webapp

COPY "start.sh" "/tmp/start.sh"
COPY "app.py" "/var/www/flaskapp/app.py"

ENTRYPOINT [ "/tmp/start.sh" ]
