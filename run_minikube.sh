#! /usr/bin/env bash

kubectl run hello-node --image=mywebserver:latest --image-pull-policy=Never

# TODO still need to expose as a service (etc etc) as per https://kubernetes.io/docs/tutorials/hello-minikube/
