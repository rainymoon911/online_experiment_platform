###uc_docker需要在OpenEdX上部署Docker,以控制另一台服务器上的Docker容器

###1.在OpenEdX上部署Docker(版本必须与Docker服务器保持一致)

参考[官方部署流程](http://docs.docker.com/installation/ubuntulinux/#ubuntu-precise-1204-lts-64-bit)

###2.在本地安装mongodb(3个XBlock都使数据库中的数据)

OpenEdX自带mongodb,无需再安装,只需建立所使用的数据库即可,使用默认端口27017

```
mongo
use test
db.token.save({username:"zyu_test"})
db.user.save({username:"zyu_test"})
db.codeview.save({username:"zyu_test"})
```

###3.uc_docker安装完毕后需要在后台创建用户可见的Docker,Docker名为ucore_lab,其余默认即可
