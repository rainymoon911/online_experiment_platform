
###1.放置脚本至指定位置

    sudo -u www-data bash
    cd /edx/var/edxapp/staticfiles
    mkdir xblock-script
    mv <path_of_code-editor>/scripts/* ./xblock-script/
    
注意:确保用户www-data拥有执行脚本的权限

###2.安装XBlock

    sudo -u edxapp /edx/bin/pip.edxapp install <path_of_xblock-codeeditor>
    
卸载命令:

    sudo -u edxapp /edx/bin/pip.edxapp uninstall jennystart-xblock
