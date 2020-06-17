#!/bin/bash
ansible server -m systemd -a 'name=kube-apiserver state=stopped'
ansible server -m systemd -a 'name=kube-controller-manager state=stopped'
ansible server -m systemd -a 'name=kube-scheduler state=stopped'
ansible server -m systemd -a 'name=kubelet state=stopped'
ansible server -m systemd -a 'name=kube-proxy state=stopped'
ansible server -m systemd -a 'name=etcd state=stopped'
ansible all -m shell -a 'rm -rf /opt/kubernetes /opt/etcd /root/ssl/ /var/run/flannel /var/lib/etcd'
ansible all -m shell -a 'ip link set dev cni0 down; ip line set dev docker0 down'
ansible all -m shell -a 'ip link delete cni0; ip link delete docker0'
ansible all -m shell -a "sed -i 's#\$DOCKER_NETWORK_OPTIONS##g' /usr/lib/systemd/system/docker.service"
ansible all -m shell -a "sed -i 's#EnvironmentFile=/run/flannel/subnet.env##g' /usr/lib/systemd/system/docker.service"