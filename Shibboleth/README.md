部署Shibboleth需要LDAP服务器,IDP服务器,以及在Gitlab,OpenEdX上分别部署SP.

更详细的文档以及配置文件可以参见[shibboleth仓库](https://github.com/rainymoon911/shibboleth-for-edx)

1.部署LDAP服务器.

1.1 安装OpenLDAP即可视化工具

[我们所使用的OpenLDAP镜像](http://www.turnkeylinux.org/openldap)

该镜像已包含phpldapadmin(方便网页端访问LDAP),若从其他渠道安装LDAP,请自行安装该工具。

1.2 利用eduperson.ldif创建模式eduPerson

    ldapadd -Y EXTERNAL -H ldapi:/// -f <path of eduperson.ldif>
    
1.3 登录管理员账号创建存储用户的结点,例如ou=Users,dc=openedx,dc=com

1.4 test_ldap.py可用于测试OpenLDAP是否正常工作(修改其中的ip,baseDN以及searchFilter参数,保持与IDP中的配置一致,
详细可参考shibboleth仓库中的配置文件)

1.5 createUser.ldif用于手动创建用户(修改其中的用户参数)
    

