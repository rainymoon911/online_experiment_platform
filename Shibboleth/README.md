部署Shibboleth需要LDAP服务器,IDP服务器,以及在Gitlab,OpenEdX上分别部署SP.
====

OpenEdX,Gitlab,idp目录包含了我们所使用的所有相关配置文件(密码使用password代替),可做参考

1.部署LDAP服务器.
====

1.1 安装OpenLDAP即可视化工具

[我们所使用的OpenLDAP镜像](http://www.turnkeylinux.org/openldap)

该镜像已包含phpldapadmin(方便网页端访问LDAP),若从其他渠道安装LDAP,请自行安装该工具。

1.2 利用eduperson.ldif创建模式eduPerson

    ldapadd -Y EXTERNAL -H ldapi:/// -f <path of eduperson.ldif>
    
1.3 登录管理员账号创建存储用户的结点,例如ou=Users,dc=openedx,dc=com

或者使用命令行添加Users节点:

	ldapadd -x -D "cn=admin,dc=edx,dc=com" -W -f create_group.ldif

1.4 test_ldap.py可用于测试OpenLDAP是否正常工作(修改其中的ip,baseDN以及searchFilter参数,保持与IDP中的配置一致,
详细可参考shibboleth仓库中的配置文件)

1.5 create_user.ldif用于手动创建用户(修改其中的用户参数)


2.部署IDP
====

2.1 安装apache 以及 tomcat:

    apt-get install apache2
    a2enmod ssl
    a2enmod proxy_ajp

    sudo apt-get install tomcat6
    
[apache和tomcat的配置](https://wiki.shibboleth.net/confluence/display/SHIB2/IdPApacheTomcatPrepare) 
    
    vi /etc/hosts
    //add the following code
    127.0.0.1 idp.edx.org sp
    
    vi /tomcat6/apache2.conf
    //add the following code
    ServerName idp.edx.org
    
    sudo vi /etc/init.d/tomcat7
    //找到JAVA_OPTS ，添加参数：-XX:+UseG1GC -Xmx1500m -XX:MaxPermSize=128m 
    JAVA_OPTS="-Djava.awt.headless=true -XX:+UseG1GC -Xmx1500m -XX:MaxPermSize=128m"
    
    sudo vi /etc/tomcat7/server.xml
    //找到 Connector ,添加属性maxPostSize ，设置值为100K(100000)
    maxPostSize="100000"
    
    sudo vi /etc/tomcat7/Catalina/localhost/idp.xml
    //添加下面的内容。idp.xml是新创建的文件
    <Context docBase="IDP_HOME/war/idp.war"
         privileged="true"
         antiResourceLocking="false"
         antiJARLocking="false"
         unpackWAR="false"
         swallowOutput="true" />
    
2.2 jdk(oracle jdk--officially recommended):

    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java7-installer
    
configure jdk

    update-alternatives --config java
    
    
2.3 idp:

我们系统间的交互是内部的,所以不使用https(所以将配置文件中的https改为了http)
(ps:SAML协议即使不使用https传输数据,也是有一定的安全性的)

2.3.1 安装idp,这里使用的版本是2.4.4

[download source](http://shibboleth.net/downloads/identity-provider/)
    
    download the source
    unzip shibboleth-identityprovider-2.4.4-bin.zip
    cd shibboleth-identityprovider-2.4.4
    JAVA_HOME=/usr/lib/jvm/java-7-oracle ./install.sh
    chown -R tomcat6:tomcat6 /opt/shibboleth-idp

访问idp.edx.org:8080//idp/profile/Status,若一切正常,可看到ok

如果出现错误,请查看日志:/opt/shibboleth-idp/logs/idp-process.log

[官方的问题解答列表](https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPTroubleshootingCommonErrors#NativeSPTroubleshootingCommonErrors-Unabletolocatemetadataforidentityprovider(https://identities.supervillain.edu/idp/shibboleth).)

idp的默认端口是8080(8443用于ECP),如果使用默认端口的话,配置文件中的idp.edx.org 需要替换为 idp.edx.org:8080



2.3.2 配置SP端的 metadata (sp的metadata生成,在安装sp的步骤中会提及)

(metadata在idp端以及sp端的名字可自行更改,但必须保持一致)

    scp sp-metadata.xml username@idp-ip:/opt/shibboleth-idp/metadata
    
    vi /conf/relying-party.xml
    //add the following code
    <metadata:MetadataProvider xsi:type="FilesystemMetadataProvider"
		xmlns="urn:mace:shibboleth:2.0:metadata" id="SPMETADATA"
		metadataFile="/opt/shibboleth-idp/metadata/sp-metadata.xml" />
		
2.3.3 配置LDAP验证

在配置前,请使用test_ldap.py保证LDAP正常工作

	vi handler.xml
	//add the following code
	<!--  Username/password login handler -->
	<ph:LoginHandler xsi:type="ph:UsernamePassword"
		jaasConfigurationLocation="file:///opt/shibboleth-idp/conf/login.config">
	<ph:AuthenticationMethod>urn:oasis:names:tc:SAML:2.0:ac:classes:
		PasswordProtectedTransport</ph:AuthenticationMethod>
	</ph:LoginHandler></code>
		
	vi attribute-resolver.xml
	//add the following code
	<resolver:DataConnector id="myLDAP" xsi:type="dc:LDAPDirectory"
        ldapURL="ldap://<your ldap url>" 
        baseDN="ou=Users,dc=openedx,dc=com" 
        principal="cn=admin,dc=openedx,dc=com"
        principalCredential="password">
        <dc:FilterTemplate>
            <![CDATA[
                (uid=$requestContext.principalName)
            ]]>
        </dc:FilterTemplate>
    	</resolver:DataConnector>
    	
    	vi attrbute-filter.xml
    	//add the following code
    	<afp:AttributeRule attributeID="email">
	    <afp:PermitValueRule xsi:type="basic:ANY" />
    	</afp:AttributeRule>

	<afp:AttributeRule attributeID="commonName">
	    <afp:PermitValueRule xsi:type="basic:ANY" />

修改attribute-resolver.xml中的ldapURL,baseDN,以及管理员名称,密码

3.SP配置(Gitlab,OpenEdX部署SP都需要此步骤作为前提)

3.1.安装

安装Apache上的shib模块

    sudo apt-get install libapache2-mod-shib2
    a2enmod shib2
    
    
    //if you don't have domain name
    vi /etc/hosts
    //add the following code
    127.0.0.1 sp.edx.org  sp
    idp-url   idp.edx.org idp
    
访问<domain of sp>/Shibboleth.sso/Status,若能显示信息,则一切正常

3.2.配置sp(你可以直接将OpenEdX或者Gitlab下的shib目录文件覆盖至你的shibboleth目录,但涉及到ip以及元数据的配置仍需要按下方提到的步骤修改)

(如果你没有将idp的端口做修改的话,那么idp默认使用8080端口, sp的配置文件中,除了已经带端口的之外,所有idp的域名都需要改成 "域名:8080" 的形式)

3.2.1

    cd <dir of sp>  //sp的路径一般为/etc/shibboleth/
    vi shibboleth2.xml
    //修改sp的entityID为你SP的域名
    <ApplicationDefaults entityID="http://sp.edx.org/shibboleth"
                         REMOTE_USER="eppn persistent-id targeted-id">
                         
    //添加 sso
    <SSO entityID="http://<domain of idp>:8080/shibboleth"
                 discoveryProtocol="SAMLDS" discoveryURL="https://ds.example.org/DS/WAYF">
              SAML2 SAML1
    </SSO>
    
    //添加 session initiator
    <SessionInitiator type="Chaining" Location="/Login" isDefault="true" id="Intranet"
		relayState="cookie" entityID="http://<domain of idp>:8080/idp/shibboleth" forceAuthn="true">
	    <SessionInitiator type="SAML2" acsIndex="1" template="bindingTemplate.html"/>
	    <SessionInitiator type="Shib1" acsIndex="5"/>
	</SessionInitiator>

3.2.2 配置元数据文件
与idp不同,sp不默认生成metadata.xml,需要手动生成。

生成密钥:

    shib-keygen -h <domain of sp>(将生成的 sp-key.pem,sp-cert.pem to移至sp的目录)
    
[about shib-keygen](http://manpages.ubuntu.com/manpages/lucid/man8/shib-keygen.8.html)

利用密钥生成 sp-metadata.xml,该文件就是配置idp时所需的sp的元数据文件

    shib-metagen -h sp.edx.org> /etc/shibboleth/sp-metadata.xml

在sp端配置idp的元数据文件,将idp服务器上的idp-metadata.xml(或者你可以为该文件重命名)复制到sp服务器上的SP目录(默认为/etc/shibboleth)

在sp端做如下修改:

    cd /etc/shibboleth/
    vi shibboleth2.xml
    //add the following code
    <MetadataProvider type="XML" file="idp-metadata.xml"/>
    
3.2.3 配置属性映射文件attribute-map.xml

    cd /etc/shibboleth/
    vi attribute-map.xml
    //add the following code
    <Attribute name="urn:oid:2.5.4.3" id="cn"/>
    <Attribute name="urn:oid:0.9.2342.19200300.100.1.3" id="mail"/>
    
3.2.4 使用shib来保护资源(这一步仅做参考,实际部署时Gitlab与Nginx略有不同)

    vi /etc/apache2/httpd.conf
    //add the following code
    <Location /secure>
    AuthType shibboleth
    ShibRequireSession On
    require valid-user
    </Location>

    cd /var/www/html(depend on your document root of apache)
    mkdir secure
    vi test.php
    //add the following code
    <?php print_r($_SERVER) ?>
    
访问<domain of sp>/secure,你将会被重定向至shibboleth认证页面成功的话,点击test.php ,你将会看到email以及cn属性。
 


4.在Gitlab上配置SP
====
[官方配置文档](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/integration/shibboleth.md)

* 先按步骤3安装SP,保证SP正常工作,将Gitlab/git_apache2目录中的文件拷贝至/etc/apache2/目录中覆盖(注意修改权限,与原文件保持一致)

  更改sites-enables/000-default 以及apache2.conf文件中的ServerName
  
       a2enmod rewrite
       a2enmod proxy

* 配置Gitlab与SP连接 

```
	vi /etc/gitlab/gitlab.rb
	//修改配置至如下
	external_url 'https://gitlab.example.com'
	gitlab_rails['internal_api_url'] = 'https://gitlab.example.com'

	# disable Nginx
	nginx['enable'] = false

	gitlab_rails['omniauth_allow_single_sign_on'] = true
	gitlab_rails['omniauth_block_auto_created_users'] = false
	gitlab_rails['omniauth_enabled'] = true
	gitlab_rails['omniauth_providers'] = [
  	  {
    		"name" => 'shibboleth',
        	"args" => {
        	"shib_session_id_field" => "HTTP_SHIB_SESSION_ID",
        	"shib_application_id_field" => "HTTP_SHIB_APPLICATION_ID",
        	"uid_field" => 'HTTP_EPPN',
        	"name_field" => 'HTTP_CN',
        	"info_fields" => { "email" => 'HTTP_MAIL'}
        	}
  	  }
	]
	//使配置生效(若此时Apache未启动,则手动启动,/etc/init.d/apache2 restart)
	sudo gitlab-ctl reconfigure

```
配置成功后,在首页可看到shibboleth字样,点击即可通过shibboleth登录

###５.在OpenEdX上配置SP  

[官方说明](https://github.com/edx/configuration/wiki/Setting-Up-External-Authentication)

* 先按步骤３配置SP
* 将OpenEdX/edx_apache2目录中的文件拷贝至/etc/apache2/目录中覆盖(注意修改权限,与原文件保持一致),并将edx_apache2/sites-available/lms中的<your domain of OpenEdX>改为OpenEdX的域名
* 复制/OpenEdX/edx_nginx/sites-available/lms 至 /etc/nginx/sites-available/
* 重启Apache以及Nginx
```
/etc/init.d/nginx restart & /etc/init.d/apache2 restart
```
* 开启shibboleth登录
```
vi /edx/app/edxapp/edx-platform/lms/envs/common.py
set 'AUTH_USE_SHIB','SHIB_DISABLE_TOS','RESTRICT_ENROLL_BY_REG_METHOD' true
```
* OpenEdX的shibboleth登录针对于某一门课程,在后台的Advanced Option中设置External Login Domain' "shib:<your idp url>"
* 在前台点击该课程,再点击登录,就会跳至shibboleth登录页面(在首页点击登录仍为正常登录方式)
