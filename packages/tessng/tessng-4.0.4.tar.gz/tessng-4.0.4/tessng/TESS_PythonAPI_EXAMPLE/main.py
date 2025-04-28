# TESS NG 二次开发说明：http://jidatraffic.com:82/
from MyTessPlugin import MyTessPlugin


if __name__ == "__main__":
    config = {
        "__netfilepath": "",  # 路网文件路径
        "__simuafterload": True,  # 加载路网后是否自动开启仿真
        "__custsimubysteps": False,  # 是否自定义仿真函数调用频率
    }
    my_tess_plugin = MyTessPlugin(config)
    my_tess_plugin.build()
