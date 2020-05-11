
FROM ubuntu:18.04

COPY . /peks

RUN apt-get update && apt-get -y upgrade
RUN /peks/pbcinstall.sh
RUN cd /peks && pip3 install -r requirements.txt
