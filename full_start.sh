#!/bin/bash

if [ $# -eq 0 ]
  then
	echo "No cluster specified given."
    exit -1
fi

set -e

source env.sh

./start_cluster.sh $1

pushd $HLF_NETWORK
if [ $# -eq 2 ]
then
	./deploy.sh -c /data/$1/hyperledger/ -b $2
else
	./deploy.sh -c /data/$1/hyperledger/
fi
popd

./deploy_on_cluster.sh

python3 add_defaults.py admin admin

set +e