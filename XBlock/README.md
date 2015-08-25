部署顺序:uc_docker->xblock-codeeditor->xblock-codebrowser
====

使xblock可用

1）edx-platform/lms/envs/common.py中去掉注释：

    # from xmodule.x_module import prefer_xmodules
  
    # XBLOCK_SELECT_FUNCTION = prefer_xmodules
  
2）edx-platform/cms/envs/common.py,中去掉注释：

    # from xmodule.x_module import prefer_xmodules
    # XBLOCK_SELECT_FUNCTION = prefer_xmodules
    
3）edx-platform/cms/envs/common.py中把

    'ALLOW_ALL_ADVANCED_COMPONENTS': False,
    改成：
    'ALLOW_ALL_ADVANCED_COMPONENTS': True,
