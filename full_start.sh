#!/bin/bash

if [ $# -eq 0 ]
  then
	echo "No cluster specified given."
    exit -1
fi

set -e

source env.sh
source versions_$1.sh

./start_cluster.sh $1

pushd $HLF_NETWORK
if [ $CHAINCODE_VERSION -eq "latest" ]
then
	./deploy.sh -c /data/$1/hyperledger/ -b $CHAINCODE_VERSION
else
	./deploy.sh -c /data/$1/hyperledger/
fi
popd

./deploy_on_cluster.sh $1

python3 add_defaults.py admin admin $1


echo
echo $HEADLINE
echo "Dashboard Token"
echo $HEADLINE

kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')

set +e