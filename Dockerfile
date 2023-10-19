FROM alpine:latest as builder
RUN apk update && \
		apk upgrade
