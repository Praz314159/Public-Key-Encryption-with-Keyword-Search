#!/bin/sh

dir=/tmp/pbcbuild
mkdir -p $dir

[ "$(id -u)" -ne 0 ] && echo "Run the script as root" && exit 1

type apt && apt update && apt install -y curl git make flex bison python3 python3-pip libgmp-dev

cd "$dir" &&
curl -LO https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz &&
tar xf pbc-0.5.14.tar.gz &&
cd pbc-0.5.14 &&
./configure --prefix=/usr && make && make install

cd "$dir" &&
git clone https://github.com/debatem1/pypbc &&
cd pypbc &&
chmod +x setup.py &&
make &&
make install

