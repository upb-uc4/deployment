# Deployment
Contains the deployment for UC4.  
`{}` is a needed parameter.  
`[]` is an optional parameter.

The current existing clusters are:
 - experimental
 - development
 - production

## Start Cluster with Hyperledger and Lagom and Co
The service versions are defined in `versions.sh`.  
The position of the Hyperledger-Deploy-Script is defined in `env.sh`.
```bash
./full_start.sh {clusterName} [chaincodeVersion]
```

## Delete a cluster
With the persistent data:
```bash
./delete_cluster.sh {clusterName}
```
Without the persistent data:
```bash
kind delete cluster --name {clusterName}
```

## Start only the cluster
```bash
./start_cluster.sh {clusterName}
```

## Select cluster for kubectl
```bash
kubectl config use-context kind-{clusterName}
```

## Deploy Lagom with Postgres and Kafka
This command deploys on the current cluster context.
```bash
./deploy_on_cluster.sh
```

## Remove specific namespaces (and everything their contain)
```bash
kind delete namespace {namespace}
```
Namespaces are:
 - uc4-lagom, every service of Lagom
 - uc4-support, supporting container like imaginary
 - hlf, everything from Hyperledger
 - postgres, everything from postgres
 - kafka, everything from kafka
 - default, traefik (not deletable)

## Restart a specific service
```bash
kubectl rollout restart deployment {serviceName} -n uc4-lagom
```

## Force a new image pull
```bash
kubectl delete deployment {serviceName} -n uc4-lagom
export {serviceName in caps}_VERSION={version}
envsubst < services/{serviceName}.yaml | kubectl apply -f -
```