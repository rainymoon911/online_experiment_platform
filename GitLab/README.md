参照[官网](https://about.gitlab.com/downloads/)的安装步骤

安装完成后,做如下修改:

1.去除邮件激活


    vi ./embedded/service/gitlab-rails/lib/api/users.rb
    
在create user函数中加入如下语句
    
    user.skip_confirmation!
    if user.save
    ...

2.使shibboleth登录的账号能与本地账号关联而不是冲突
