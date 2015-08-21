部署Shibboleth需要LDAP服务器,IDP服务器,以及在Gitlab,OpenEdX上分别部署SP.

更详细的文档以及配置文件可以参见[shibboleth仓库](https://github.com/rainymoon911/shibboleth-for-edx)

1.部署LDAP服务器.

[我们所使用的OpenLDAP镜像](http://www.turnkeylinux.org/openldap)

该镜像已包含phpldapadmin,若从其他渠道安装LDAP,请自行安装该工具。
