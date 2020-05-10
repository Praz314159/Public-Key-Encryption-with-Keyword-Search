
FROM ubuntu:18.04

COPY . /peks

RUN apt-get update && apt-get -y upgrade
RUN /peks/pbcinstall.sh
