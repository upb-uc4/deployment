#!/bin/bash
source env.sh

echo
echo $HEADLINE
echo "Starting Traefik"
echo $HEADLINE
kubectl apply -f traefik/ingress-route.yaml
kubectl apply -f traefik/traefik-service.yaml
kubectl apply -f traefik/traefik-deployment.yaml
kubectl apply -f traefik/traefik-router.yaml

echo
echo $HEADLINE
echo "Starting Support"
echo $HEADLINE
kubectl create namespace uc4-support
kubectl apply -f support/imaginary.yaml

echo
echo $HEADLINE
echo "Starting Postgres"
echo $HEADLINE
kubectl create namespace postgres
kubectl apply -f postgres/postgres-config.yaml
kubectl apply -f postgres/postgres-configmap.yaml
kubectl apply -f postgres/postgres-storage.yaml
kubectl apply -f postgres/postgres-deployment.yaml
kubectl apply -f postgres/postgres-service.yaml

echo
echo $HEADLINE
echo "Starting Kafka"
echo $HEADLINE
kubectl create namespace kafka
kubectl apply -f kafka/kafka.yaml  -n kafka
sleep 10
kubectl apply -f kafka/kafka-single.yaml  -n kafka

echo
echo $HEADLINE
echo "Wait for Kafka & Postgres"
echo $HEADLINE
(
	kubectl wait --for=condition=Ready pods --all --timeout=300s -n postgres
	kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s  -n kafka
) || (
	echo "Waiting error, trying again in a few seconds"
	sleep 2
	kubectl wait --for=condition=Ready pods --all --timeout=300s -n postgres
	kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s  -n kafka
) || (
	echo "Waiting error, trying again in a few seconds"
	sleep 10
	kubectl wait --for=condition=Ready pods --all --timeout=300s -n postgres
	kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s  -n kafka
) || (
	echo "Waiting failed"
	exit -1
)
sleep 60

echo
echo $HEADLINE
echo "Set RBAC"
echo $HEADLINE
kubectl create namespace uc4-lagom
kubectl apply -f rbac.yaml

echo
echo $HEADLINE
echo "Starting Services"
echo $HEADLINE

source versions.sh

kubectl create secret generic application-secret --from-literal=secret="$(openssl rand -base64 48)" -n uc4-lagom
kubectl create secret generic uc4-master-secret --from-literal=secret="$(openssl rand -base64 48)" -n uc4-lagom
kubectl create secret generic uc4-kafka-salt --from-literal=secret="$(openssl rand -base64 48)" -n uc4-lagom

kubectl apply -f secrets/user.yaml
envsubst < services/user.yaml | kubectl apply -f -

kubectl apply -f secrets/authentication.yaml
envsubst < services/authentication.yaml | kubectl apply -f -

kubectl apply -f secrets/course.yaml
envsubst < services/course.yaml | kubectl apply -f -

envsubst < services/matriculation.yaml | kubectl apply -f -

kubectl apply -f secrets/certificate.yaml
envsubst < services/certificate.yaml | kubectl apply -f -

envsubst < services/configuration.yaml | kubectl apply -f -

kubectl apply -f secrets/examreg.yaml
envsubst < services/examreg.yaml | kubectl apply -f -