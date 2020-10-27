
#/usr/bin/python3

import os
import hashlib
import time
import kubernetes.config
import kubernetes.client
from crontab import CronTab

def hash(str_to_hash):
    hash_object = hashlib.sha256(str(str_to_hash).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def getContainerImageListnames():
    containerNames = [] 

    # Local
    #kubernetes.config.load_kube_config()

    # Inside the cluster
    kubernetes.config.load_incluster_config()

    node_name = os.environ.get('MY_NODE_NAME', None)
    v1 = kubernetes.client.CoreV1Api()    
    print("Listing containers for pods on node: ", node_name)
    field_selector = "spec.nodeName=" + node_name
    ret = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for i in ret.items:
        for j in i.spec.containers:
            containerNames.append(j.image)

    return containerNames


def scanContainerImage(imageName):
    os.system("trivy image -f json  " + imageName + " > " + hash(imageName) + ".json")


def main():
    cron = CronTab(user=True)
    names = getContainerImageListnames()
    for i in names:
        print("%s\t" % (i))
        # scanContainerImage(i)
        job = cron.new(command="trivy image -f json  " + i + " > " + hash(i) + ".json")
        job.minute.every(10)
        cron.write()
    
    while True:
        time.sleep(5)  


if __name__ == '__main__':
    main()

