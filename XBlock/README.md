部署顺序:uc_docker->xblock-codeeditor->xblock-codebrowser
====

[部署文件备份,供参考](https://github.com/rainymoon911/online_experiment_platform/tree/master/OpenEdX/edx_config.backup)

###使xblock可用

* edx-platform/lms/envs/common.py中去掉注释：

        #from xmodule.x_module import prefer_xmodules
  
        #XBLOCK_SELECT_FUNCTION = prefer_xmodules
  
* edx-platform/cms/envs/common.py,中去掉注释：

        #from xmodule.x_module import prefer_xmodules
        #XBLOCK_SELECT_FUNCTION = prefer_xmodules
    
* edx-platform/cms/envs/common.py中把

        'ALLOW_ALL_ADVANCED_COMPONENTS': False,
        改成：
        'ALLOW_ALL_ADVANCED_COMPONENTS': True,
    

###XBlock安装完成后需重启服务:

    sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
    sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp_worker:
