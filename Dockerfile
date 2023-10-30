FROM alpine:3.18 as builder

### Update and install env
RUN apk update && \
    apk upgrade && \
    apk add gcc linux-headers && \
    apk add python3-dev py3-psutil
      
RUN   python -m ensurepip --upgrade
COPY  requirements.txt ./
RUN   /usr/bin/pip3 install -r  ./requirements.txt

### Create non-root user
ARG MY_USER
ARG MY_GROUP
ARG MY_UID
ARG MY_GID
RUN addgroup -g $MY_GID $MY_GROUP && \
	  adduser -u $MY_UID $MY_USER -G $MY_GROUP -D

USER  $MY_USER
WORKDIR /home/$MY_USER/
