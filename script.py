
#/usr/bin/python3

import os
import hashlib
import kubernetes.config
import kubernetes.client


def hash(str_to_hash):
    hash_object = hashlib.sha256(str(str_to_hash).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def getContainerImageListnames():
    containerNames = [] 

    # Local
    kubernetes.config.load_kube_config()

    # Inside the cluster
    # kubernetes.config.load_incluster_config()

    v1 = kubernetes.client.CoreV1Api()    
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        for j in i.spec.containers:
            containerNames.append(j.image)

    return containerNames


def scanContainerImage(imageName):
    os.system("trivy image -f json  " + imageName + " > " + hash(imageName) + ".json")


def main():
    names = getContainerImageListnames()
    for i in names:
        print("%s\t" % (i))
        scanContainerImage(i)


if __name__ == '__main__':
    main()

