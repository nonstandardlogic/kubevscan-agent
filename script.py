
# /usr/bin/python3

import os
import sys
import hashlib
import time

from timeloop import Timeloop
from datetime import timedelta

import kubernetes.config
import kubernetes.client
from os import path


imgListNames = []
tl = Timeloop()


def hash(str_to_hash):
    hash_object = hashlib.sha256(str(str_to_hash).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


def getContainerImageListnames():
    containerNames = []

    # Local
    # kubernetes.config.load_kube_config()

    # Inside the cluster
    kubernetes.config.load_incluster_config()

    try:
        os.environ["MY_POD_NAME"]
    except KeyError:
        print("Please set the environment variable MY_POD_NAME")
        sys.exit(1)

    pod_name = os.environ.get('MY_POD_NAME')
    v1 = kubernetes.client.CoreV1Api()
    print(f'Listing containers for pod : {pod_name}')
    fs = "metadata.name=" + pod_name
    ret = v1.list_pod_for_all_namespaces(watch=False, field_selector=fs)
    for i in ret.items:
        for j in i.spec.containers:
            containerNames.append(j.image)
            print(f'Img {j.image} pod {i.metadata.name}')

    return containerNames


@tl.job(interval=timedelta(seconds=30))
def scheduled_job():
    global imgListNames
    print(f'Ctime : {format(time.ctime())} Img count : {len(imgListNames)}')
    for i in imgListNames:
        print("Scanning %s\t" % (i))
        scanContainerImage(i)


def scanContainerImage(i):
    h = hash(i)
    os.system("trivy image -f json " + i + " > " + "/var/log/kubevscan/" + h + ".json")


def main():
    global imgListNames
    imgListNames = getContainerImageListnames()

    logPath = "/var/log/kubevscan"
    if (path.isdir(logPath) is False):
        os.mkdir(logPath)

    tl.start(block=True)


if __name__ == '__main__':
    main()
