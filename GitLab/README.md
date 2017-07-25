参照[官网](https://about.gitlab.com/downloads/)的安装步骤
[中文版安装步骤整理](http://blog.csdn.net/jenyzhang/article/details/52353355)

####1. 安装前查看端口状态，并把80和8080端口解除占用
   由于gitlab安装结束后会占用80和8080端口，所以如果你的操作系统中己有apache,tomcat那么这两个端口是处于占用状态的，会导致安装gitlab后访问localhost时出现502错误。因此，我们先释放这两个端口。
   
输入下面的命令查看端口状态：

```sudo netstat -anptl```

然后找到80,和8080端口对应的pid (如果显示这两个端口被占用，则用下面的命令杀死进程解除端口占用)

输入：```kill -9 <pid>```  //如果pid为1213，则输入kill -9 1213
 
####2. 安装和配置必要的依赖
输入下面的命令：

```sudo apt-get install curl openssh-server ca-certificates postfix  ```

如果要安装Postifx 来发送邮件，在安装过程中选择“Internet Site”。 也可以使用Sendmail,或者配置客户端SMTP 服务器来发送邮件。

####3.添加gitlab 包服务并安装包
 输入下面的命令
 
 ```curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash```
 
 然后输入下面的命令安装包：
 
 ```sudo apt-get install gitlab-ce  ```
 
 
####4. 配置并重启Gitlab
 
  输入下面的命令:
  
  ```sudo gitlab-ctl reconfigure```
  
  
####5. 访问http://locahost
 首次访问gitlab,会直接重定向到设置密码屏幕，初始用户名是root。
 如果上述正常，则gitlab己安装好
 
 关于gitlab安装更详细的描述可参看此文章：[http://blog.csdn.net/jenyzhang/article/details/52353355](http://blog.csdn.net/jenyzhang/article/details/52353355)
 
 
 ------------------------------------------------------------------------------------------------------------------------------------

git_config.backup目录中为Gitlab服务器上的配置文件备份


安装完成后,做如下修改:

[user.rb备份](https://github.com/rainymoon911/online_experiment_platform/blob/master/GitLab/git_config.backup/users.rb)

1.去除邮件激活


    vi ./embedded/service/gitlab-rails/lib/api/users.rb
    
在create user函数中加入如下语句
    
    user.skip_confirmation!
    if user.save
    ...

[gitlab.rb备份](https://github.com/rainymoon911/online_experiment_platform/blob/master/GitLab/git_config.backup/gitlab.rb)

2.去除前台的注册功能(默认是关闭的,若开启,按下列步骤关闭)

    vi /etc/gitlab/gitlab.rb
    gitlab_rails['gitlab_signup_enabled'] = false
    //使配置生效
    sudo gitlab-ctl reconfigure

3.配置不允许用户修改邮件:

    vi /etc/gitlab/gitlab.rb
    gitlab_rails['gitlab_username_changing_enabled'] = false
    //使配置生效
    sudo gitlab-ctl reconfigure
    
4.去除邮件查重(由于shibboleth登录时会报邮件已存在的错误,不像OpenEdX能与本地账号绑定)

5.创建教师账号,用户名teacher,教师以管理员的账号在Docker的配置文件中会用到
