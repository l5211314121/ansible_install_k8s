FROM centos:7


ADD ansible_install_k8s /usr/bin/
CMD ["sleep", "3600"]
