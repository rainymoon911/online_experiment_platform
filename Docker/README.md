###部署Docker服务器(推荐使用CentOS 7)

* 安装Docker,[官方部署流程](http://docs.docker.com/installation/)

* 创建密钥
  编辑脚本`scripts/pemgen.sh`，设置环境变量`UC_DOMAIN`为Docker服务器的域名  
  执行脚本`scripts/pemgen.sh`，然后将会在`scripts/certs`文件夹下看到生成的若干密钥
* 使用以下命令，启动Docker服务：  
```
$sudo docker -d --tlsverify --tlscacert=<ca.pem> --tlscert=<server-cert.pem> --tlskey=<server-key.pem> -H=0.0.0.0:2376
```
* 访问Docker服务器，添加默认镜像，在`scripts`目录下找到Dockerfile文件，执行： 
```
$sudo docker --tlsverify -H=<docker-server>:<port> --tlscacert=<ca.pem> --tlscert=<cert.pem> --tlskey=<key.pem> pull docker.io/fedora:21
```
```
$sudo docker --tlsverify -H=<docker-server>:<port> --tlscacert=<ca.pem> --tlscert=<cert.pem> --tlskey=<key.pem> build --rm -t uclassroom/ucore-vnc-base .
```
