#!/bin/sh

tmp="$(mktemp -u)"
mkfifo "$tmp"
trap "rm -f $tmp" EXIT

out="$(date '+timings--%Y-%m-%d--%H-%M-%S.csv')"
echo "MODE,SP,N,GEN,PEKS,TRAPDOOR,TEST" > "$out"

# mode = bm
for sp in 80 160 240 320 400 512 600; do
	for n in $(python -c "for i in range(8): print(2**i)"); do
		parallel -j8 "mkfifo /tmp/{} 2>/dev/null; seq $n > /tmp/{} & python ../peks.py -sp $sp -m bm -t nope -kf /tmp/{} --time >> $out" ::: $(seq 50)
	done
done

# mode = td
for sp in 1024 2048 4096; do
	for n in $(python -c "for i in range(8): print(2**i)"); do
		parallel -j8 "mkfifo /tmp/{} 2>/dev/null; seq $n > /tmp/{} & python ../peks.py -sp $sp -m td -t nope -kf /tmp/{} --time >> $out" ::: $(seq 50)
	done
done
