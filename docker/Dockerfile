FROM golang:1.14-alpine
LABEL maintainer="Sam Hoffman <sam@codewizardshq.com>"

ENV LANGUAGE=""
ENV CODEFILE=""
ENV TIMEOUT="5"
ENV DEBUG="0"
VOLUME "/mnt/code"

RUN apk --update add --no-cache python3 bash binutils libc-dev python3-dev gcc git libseccomp-dev strace
RUN pip3 install -U pip
RUN pip3 install pyduktape

WORKDIR "/go/src/app"
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...
RUN go build -o main .

# uncomment for debugging
# CMD [ "strace", "-fqxy", "-a0", "-s32", "/go/src/app/main"]

CMD ["/go/src/app/main"]
