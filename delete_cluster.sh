#!/bin/bash

if [ $# -eq 0 ]
  then
	echo "No cluster specified given."
    exit -1
fi

source env.sh

echo
echo $HEADLINE
echo "Delete Cluster"
echo $HEADLINE

kind delete cluster --name $1
rm "/data/$1" -r