# pyapollo

Apollo配置读取
支持admin和config单独配置服务
支持配置namespace和排除的namespace
支持key watch变更，支持logger传入
支持将apollo配置变更同步到config类


Project description
apollo-client3 - Python Client for Ctrip's Apollo

方便Python接入配置中心框架 Apollo 所开发的Python版本客户端。 Tested with python 3.10+

基于https://github.com/filamoon/pyapollo/ 修改

Installation
```
pip install apollo-client3
```
Features
实时同步配置
灰度配置
客户端容灾
Usage
```
<!-- 启动客户端长连接监听 -->
from pyapollo import ApolloClient
client = ApolloClient(app_id=<appId>, cluster=<clusterName>, config_server_url=<configServerUrl>)
client.start()
<!-- 获取Apollo的配置 -->

client.get_value(Key, DefaultValue, namespace)
```
# 配置
```
from pyapollo import ApolloClient
apolloClient = ApolloClient(app_id='EZR.Arch.ECollectRCsms.ApiHost',
                                config_server_url='http://192.168.128.156:8080',
                                admin_server_url='http://192.168.12.127:8090',
                                env='FAT',
                                cycle_time=10,
                                exceptNamespaces='Architecture.Common',
                                logger=None,
                                timeout=6)
class config:
    WorkTime='1234'
c=config()
apolloClient.add_listener(c)
apolloClient.start()
apolloClient.watch_key_change('WorkTime',lambda x:print(f'WorkTime is changed to {x}'))

import time
while True:
    time.sleep(5)
    v = apolloClient.get_value('WorkTime','1')
    print('---------',v)
    print('----c.WorkTime-----',c.WorkTime)
```


Reference
Apollo : https://github.com/ctripcorp/apollo

Contributor
Bruce
prchen
xhrg
johnliu

Version log
11/24/2019 Bruce 0.8.2 优化本地缓存的存储方式
1/4/2020 Bruce 0.8.4 修复文件读取异常的bug
3/24/2020 prchen 0.8.5 修复安装过程中requests模块依赖的问题
7/5/2020 Bruce 0.9 主线程退出时，关闭获取配置的子线程
25/5/2020 xhrg 0.9.1 修复文件名称读取异常
13/7/2020 Bruce 0.9.2 【bugfix】修复当namespace不存在时，服务器挂起导致get_value无响应
18/10/2020 Bruce 2.0 重构 | 优化数据获取方式 ｜ 优化定时任务 | 新增authorization传入
04/29/2025 Johnliu 升级支持python3.10，重构，支持admin和config单独配置服务，支持配置namespace和排除的namespace，支持key watch变更，支持logger传入，支持将apollo配置变更同步到config类，修复本地配置文件读取报错