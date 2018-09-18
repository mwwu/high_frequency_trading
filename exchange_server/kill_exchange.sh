#!/bin/sh

if [ "$#" -ne 2 ]; then
        echo "usage: ./kill_echange.sh [exchange] [# of groups]"
        exit 1
fi

exchange_type=$1
groups=$2

if [ "$exchange_type" = "CDA" ]; then
        port=900
fi
if [ "$exchange_type" = "FBA" ]; then
        port=910
fi

for i in `seq $groups`;
do
	PID=`lsof -i tcp:$port$i | awk '$8 == "TCP" { print $2 }'`
        kill $PID
done