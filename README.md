### 使用方法
准备一个`inventory file`，文件中写明各个组件对应的地址，etcd的地址后需要添加一个etcdname用来标识etcd，下面是一个etcd的示例：
```
[all]
172.26.50.248
172.26.234.10
172.26.50.247

[node]
172.26.234.10
172.26.50.247

[ansible]
172.26.50.248

[server]
172.26.50.248

[etcd]
172.26.50.248 etcdname=etcd01
172.26.234.10 etcdname=etcd02
172.26.50.247 etcdname=etcd03

[new-node]
172.26.50.248
```

如果需要安装所有的组件，那么你可以直接执行`ansible-play site.yaml`命令，不需要指定任何的tag。如果需要安装特定的组件或者运行特定的功能，那么需要指定具体的tag。例如`ansible-play site.yaml -t install_node`命令会在指定的机器安装node组件。

### 新增node机器
新增node节点，需要在inventory文件中，将新机器的地址写入到`new-node`组中，然后执行`ansible-play new-node site.yaml -t install_node`命令即可


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
| install_node | 配置node节点包括kubelet，kube-proxy |
| install_kubelet | 安装kubelet |
| install_kube_proxy | 安装kube-proxy |