代码编辑器XBlock
======

###1.首先安装Woboq codebrowser及其所需的环境

[官方配置文档](https://github.com/woboq/woboq_codebrowser/)

###2.创建代码以及浏览页面的存放目录

    sudo -u www-data bash
    cd <path of xblock-codebrowser>
    ./scripts/create_dir.sh
    cp -r your_woboq_codebrowser_file/* /edx/var/edxapp/woboq_codebrowser/
    mv ./scripts/generator.sh /edx/var/edxapp/staticfiles/xblock-script/
    mv ./scripts/make.sh /edx/var/edxapp/staticfiles/xblock-script/

注意:必须确保www-data用户拥有scripts中脚本的执行权限以及所创建目录的读写权限

###3.替换学生界面的code-editor XBlock的URL

* 在部署完code-editor之后记录下该学生页面该XBlock对应的URL,并做如下操作:

    vi <path_of_xblock-codebrowser>/codebrowser/static/js/src/codebrowser_view.js>

* 将如下语句中的URL替换成code-editor对应的URL,

    window.location.href = "http://166.111.68.45:11133/courses/BIT/CS101/2014T1/courseware/0b64b532c9f44b2c9c23a87a2b1f8104/da4d2d1648bf49baa59c08715acfcd38/";
    
###4.安装XBlock

    sudo -u edxapp /edx/bin/pip.edxapp install <path_of_xblock-codebrowser>

卸载命令:

    sudo -u edxapp /edx/bin/pip.edxapp uninstall xblock-codebrowser
    

    

    
    
    



