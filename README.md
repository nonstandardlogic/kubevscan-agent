# kubevscan-agent

## What is this ?

kubevscan-agent is a simple vulnerability scanner for Kubernetes cluster.

kubevscan-agent is deployed in a Kubernetes cluster.

kubevscan-agent container scans the vulnerabilities of the containers contained in the same pod.

kubevscan-agent get the list of images on which the containers are based and then executes a python script which invokes the Trivy tool on each image.

## Installation

A Makefile is provided. 

Build and push the image :

    $ make docker-build
    $ make docker-push

Deploy the kubernetes ressources

    $ kubectl apply -f kubernetes/cluster-role.yaml
    $ kubectl apply -f kubernetes/role-binding.yaml
 
# Run

Deploy the pod which contains kubevscan-agent

    $ kubectl apply -f kubernetes/deployment-test.yaml


Kubevscan creates a log file for each image. 
The name of the log file is produced by the hash code of the image name. 
The log files are stored in the */var/log/kubevscan* directory







