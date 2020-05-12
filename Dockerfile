
FROM ubuntu:18.04

COPY . /peks

RUN apt-get update \
    && apt-get -y upgrade \
    && /peks/pbcinstall.sh \
    && cd /peks \
    && pip3 install -r requirements.txt \
    && ln -sv /usr/bin/python3 /usr/bin/python
