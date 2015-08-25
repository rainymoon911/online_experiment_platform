###uc_docker需要在OpenEdX上部署Docker,以控制另一台服务器上的Docker容器

###1.在OpenEdX上部署Docker

参考[官方部署流程](http://docs.docker.com/installation/ubuntulinux/#ubuntu-precise-1204-lts-64-bit)


###2.部署Docker服务器(推荐使用CentOS 7)

* 同样先安装Docker(版本必须与上一步的Docker保持一致)

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

###3.在本地安装mongodb(3个XBlock都使数据库中的数据)

OpenEdX自带mongodb,无需再安装,只需建立所使用的数据库即可,使用默认端口27017

```
mongo
use test
db.token.save({username:"zyu_test"})
db.user.save({username:"zyu_test"})
db.codeview.save({username:"zyu_test"})
```

###4.uc_docker安装完毕后需要在后台创建用户可见的Docker,Docker名为ucore_lab,其余默认即可
