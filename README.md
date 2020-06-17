# 使用ansible通过二进制形式安装k8s

### 使用方法
命令示例：`ansible-play -i inventory etcd site.yaml -t init`

### 参数
- `-i inventory etcd`表示ansible的host文件，`inventory`中需要有ansible, all, etcd, server, node这几个组，其中ansible表示ansible主控机，all表示所有机器，etcd表示etcd的机器，server表示所有master机器，node表示所有node机器， 如果`inventory`为`/etc/ansible/hosts`则`-i inventory`可以忽略；etcd为inventory文件中组的名字
- `-t init`表示使用的tag，例如只需要进行机器的初始化，那么只需要使用`-t init`标签，

### 现有标签
| 标签名 | 含义 |
| --- | --- |
| certs | 生成证书，包括apiserver，admin，etcd，kube-proxy的证书|
| admin_certs | 生成admin证书， admin证书用于生成kubectl的kubeconfig文件，管理集群使用的证书|
| server_ca_certs | 生成apiserver的证书 |
| kube_proxy_certs | 生成kube-proxy的证书 |
| etcd_certs | 生成etcd的证书 |
| install_etcd | 安装etcd |
| restart_etcd | 重启etcd |
| set_network | 写入flannel网段信息到etcd |
| install_flannel | 安装flannel |
| change_docker_script | 修改docker启动脚本，添加flannel相关信息 |
| restart_flanneld | 重启flannel |
| init | 初始化机器，包括创建存放安装包的目录，存放配置文件和证书的目录，安装docker等 |
| mkdir | 初始化机器只创建目录 |
| init_ansible | 初始化ansible主控机，包括创建存放安装包的目录，安装golang、cfssl |
| install_server | 安装apiserver，controller-manager，scheduler |
| install_apiserver | 安装apiserver |
| restart_apiserver | 重启apiserver |
| install_controller_manager | 安装controller-manager |
| install_scheduler | 安装scheduler |