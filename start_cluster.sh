#!/bin/bash

if [ $# -eq 0 ]
  then
	echo "No cluster specified given."
    exit -1
fi

echo
echo $HEADLINE
echo "Start Cluster"
echo $HEADLINE

kind create cluster --name $1 --config "clusters/$1_cluster_config.yaml"