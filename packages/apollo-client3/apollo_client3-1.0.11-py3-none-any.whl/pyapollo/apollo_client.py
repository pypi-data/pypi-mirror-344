#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/
# @Author  : Lin Luo/ Bruce Liu
# @Email   : 15869300264@163.com
import copy
import json
import logging
import os
import threading
import time
from telnetlib import Telnet
from typing import Any, Dict, List, Optional

import requests

from .exceptions import (BasicException, NameSpaceNotFoundException,
                         ServerNotResponseException)

class ApolloClient(object):
    """
    this module is modified from the project: https://github.com/filamoon/pyapollo
    and had commit the merge request to the original repo
    thanks for the contributors
    since the contributors had stopped to commit code to the original repo, please submit issue or commit to https://github.com/BruceWW/pyapollo
    """

    def __new__(cls, *args, **kwargs):
        """
        singleton model
        """
        tmp = {_: kwargs[_] for _ in sorted(kwargs)}
        key = f"{args},{tmp}"
        if hasattr(cls, "_instance"):
            if key not in cls._instance:
                cls._instance[key] = super().__new__(cls)
        else:
            cls._instance = {key: super().__new__(cls)}
        return cls._instance[key]

    def __init__(
        self,
        app_id: str,
        cluster: str = "default",
        config_server_url: str = "",
        admin_server_url: str = "",
        env: str = "DEV",
        namespaces: List[str] = None,
        ip: str = None,
        timeout: int = 60,
        cycle_time: int = 300,
        cache_file_path: str = None,
        authorization: str = None,
        exceptNamespaces: List[str] = None,
        logger = None
        # request_model: Optional[Any] = None,
    ):
        """
        init method
        :param app_id: application id
        :param cluster: cluster name, default value is 'default'
        :param config_server_url: with the format 'http://localhost:80080'
        :param env: environment, default value is 'DEV'
        :param timeout: http request timeout seconds, default value is 60 seconds
        :param ip: the deploy ip for grey release, default value is the local ip
        :param cycle_time: the cycle time to update configuration content from server
        :param cache_file_path: local cache file store path
        :param namespaces: 如果不配置管理链接，可以直接配置固定namespaces
        :param exceptNamespaces: 不需要监控的命名空间
        """
        self.logger:logging.Logger=None
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("pyapollo")
        self.config_server_url = config_server_url
        self.admin_server_url = admin_server_url
        if not admin_server_url and not config_server_url:
            raise Exception("apollo admin_server_url and config_server_url can not be all empty")
        self.app_id = app_id
        self.cluster = cluster
        self.timeout = timeout
        self.stopped = False
        self._env = env
        self.ip = self.init_ip(ip)
        remote = self.config_server_url.split(":")
        self.host = f"{remote[0]}:{remote[1]}"
        self.exceptNamespaces= exceptNamespaces
        self.namespaces=[]
        if namespaces:
            self.namespaces = {namespace: 1 for namespace in namespaces}
        elif not admin_server_url and not self.namespaces:
            raise Exception("apollo admin_server_url can not be empty when namespaces is empty")
        if len(remote) == 1:
            self.port = 8090
        else:
            self.port = int(remote[2])
        self._authorization = authorization

        self._request_model = None
        self._cache: Dict = {}
        self._notification_map = {}
        # if namespaces is None:
        #     namespaces = ["application"]
        # self._notification_map = {namespace: -1 for namespace in namespaces}
        self._cycle_time = cycle_time
        self._hash: Dict = {}
        if cache_file_path is None:
            self._cache_file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "config"
            )
        else:
            self._cache_file_path = cache_file_path
        self.listen_configs=[]
        self.key_change_event = {}
        self.logger.info(f"apollo cache path is {self._cache_file_path}")
        self._path_checker()
        # for http request extension
        # self.start()

    def _get_clusters(self) -> dict:
        """
        get clusters by app id
        :return :
        """
        url = f"{self.host}:{self.port}/apps/{self.app_id}/clusters"
        r = self._http_get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return {}
    def add_listener(self, listener):
        self.listen_configs.append(listener)
    def watch_key_change(self,key,func):
        '''监控某个key的变更，处理'''
        self.key_change_event[key]=func
    def _update_listener(self, settings:dict):
        for listener in self.listen_configs:
            for key in dir(listener):
                try:
                    if not key.startswith('__') and not callable(getattr(listener, key)):
                        default_val = getattr(listener, key)
                        # 优先读取环境变量
                        val = os.environ.get(key)
                        if val is None:
                            # 环境变量不存在则读取Apollo
                            try:
                                val = settings.get(key, str(default_val)) if default_val is not None else settings.get(key)
                            except Exception as e:
                                logging.warning(f"Apollo获取配置失败 [{key}]: {str(e)}")
                                val = default_val
                        if isinstance(default_val, (int, float)):
                            try:
                                val = type(default_val)(val)  # 保持原始类型
                            except ValueError:
                                logging.warning(f"环境变量类型转换失败 [{key}]")
                        if default_val!=val:
                            if key in self.key_change_event:
                                try:
                                    if self.key_change_event[key]:
                                        self.logger.info(f"Apollo更新{listener.__class__.__name__}配置{key}值由:{default_val} 变更为：{val}")
                                        self.key_change_event[key](val)
                                except:
                                    self.logger.error(f"Apollo执行{key}值变更失败: {e}")
                        setattr(listener, key, val)
                except Exception as e:
                    if isinstance(listener,type):
                        self.logger.error(f"Apollo更新{listener.__class__.__name__}配置{key}失败: {e}")
                    else:
                        self.logger.error(f"Apollo更新{listener}配置{key}失败: {e}")

    def _get_namespaces(self) -> dict:
        """
        get namespaces by app id and cluster
        :return :
        """
        if self.namespaces:
            return copy.copy(self.namespaces)
        if self.admin_server_url:
            url = f"{self.admin_server_url}/apps/{self.app_id}/clusters/{self.cluster}/namespaces"
            r = self._http_get(url)
            if r.status_code == 200:
                namespaces = r.json()
                return {_.get("namespaceName"): _.get("id") for _ in namespaces}
            else:
                return {"application": -1}
        else:
            raise Exception("apollo admin_server_url can not be empty when namespaces is empty")
            

    @staticmethod
    def init_ip(ip: Optional[str]) -> str:
        """
        for grey release
        :param ip:
        :return:
        """
        if ip is None:
            try:
                import socket

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 53))
                ip = s.getsockname()[0]
                s.close()
            except BaseException:
                return "127.0.0.1"
        return ip

    def get_value(
        self, key: str, default_val: str = None, namespace: str = "application"
    ) -> Any:
        """
        get the configuration value
        :param key:
        :param default_val:
        :param namespace:
        :return:
        """
        try:
            # check the namespace is existed or not
            if namespace in self._cache:
                return self._cache[namespace].get(key, default_val)
            return default_val
        except BasicException:
            return default_val

    def start(self) -> None:
        """
        Start the long polling loop.
        :return:
        """
        # check the cache is empty or not
        if len(self._cache) == 0:
            self._long_poll()
        # start the thread to get config server with schedule
        t = threading.Thread(target=self._listener)
        t.setDaemon(True)
        t.start()

    def _http_get(self, url: str, params: Dict = None) -> requests.Response:
        """
        handle http request with get method
        :param url:
        :return:
        """
        if self._request_model is None:
            return self._request_get(url, params=params)
        else:
            return self._request_model(url)

    def _request_get(self, url: str, params: Dict = None) -> requests.Response:
        """

        :param url:
        :param params:
        :return:
        """
        try:
            if self._authorization:
                return requests.get(
                    url=url,
                    params=params,
                    timeout=self.timeout // 2,
                    headers={"Authorization": self._authorization},
                )
            else:
                return requests.get(url=url, params=params, timeout=self.timeout // 2)

        except requests.exceptions.ReadTimeout:
            # if read timeout, check the server is alive or not
            try:
                tn = Telnet(host=self.host, port=self.port, timeout=self.timeout // 2)
                tn.close()
                # if connect server succeed, raise the exception that namespace not found
                raise NameSpaceNotFoundException("namespace not found")
            except ConnectionRefusedError:
                # if connection refused, raise server not response error
                raise ServerNotResponseException(
                    "server: %s not response" % self.config_server_url
                )

    def _path_checker(self) -> None:
        """
        create configuration cache file directory if not exits
        :return:
        """
        if not os.path.isdir(self._cache_file_path):
            os.mkdir(self._cache_file_path)

    def _update_local_cache(
        self, release_key: str, data: str, namespace: str = "application"
    ) -> None:
        """
        if local cache file exits, update the content
        if local cache file not exits, create a version
        :param release_key:
        :param data: new configuration content
        :param namespace::s
        :return:
        """
        # trans the config map to md5 string, and check it's been updated or not
        if self._hash.get(namespace) != release_key:
            self._update_listener(data)
            # if it's updated, update the local cache file
            with open(
                os.path.join(
                    self._cache_file_path,
                    "%s_configuration_%s.txt" % (self.app_id, namespace),
                ),
                "w",
            ) as f:
                new_string = json.dumps(data)
                f.write(new_string)
            self._hash[namespace] = release_key

    def _get_local_cache(self, namespace: str = "application") -> Dict:
        """
        get configuration from local cache file
        if local cache file not exits than return empty dict
        :param namespace:
        :return:
        """
        try:
            cache_file_path = os.path.join(
                self._cache_file_path, "%s_configuration_%s.txt" % (self.app_id, namespace)
            )
            if os.path.isfile(cache_file_path):
                with open(cache_file_path, "r") as f:
                    result = json.loads(f.readline())
                return result
            return {}
        except Exception as ex:
            self.logger.error("get local cache error: %s" % ex)
    def _get_config_by_namespace(self, namespace: str = "application") -> None:
        """

        :param namespace:
        :return:
        """
        url = ''
        if self.config_server_url:
            releaseKey = self._hash.get(namespace)
            url = f"{self.config_server_url}/configs/{self.app_id}/{self.cluster}/{namespace}?releaseKey={releaseKey}&ip={self.ip}"
        else:
            url = f"{self.admin_server_url}/apps/{self.app_id}/clusters/{self.cluster}/{namespace}/releases/latest"
        try:
            r = self._http_get(url)
            if r.status_code == 200:
                data = r.json()
                configurations = data.get("configurations")
                if not configurations:
                    return
                if isinstance(configurations, str):
                    configurations = json.loads(configurations)
                self._cache[namespace] = configurations
                self.logger.info(
                    "Updated local cache for namespace %s release key %s: %s",
                    namespace,
                    data["releaseKey"],
                    repr(self._cache[namespace]),
                )
                self._update_local_cache(
                    data.get("releaseKey", str(time.time())),
                    data.get("configurations", {}),
                    namespace,
                )
            elif r.status_code != 304:
                print(r.text)
                self.logger.info(f"get configuration from config server {url} failed, status code %s", r.status_code)
                data = self._get_local_cache(namespace)
                self.logger.info(f"get configuration from local cache file {self._cache_file_path}")
                self._cache[namespace] = data
        except BaseException as e:
            self.logger.warning(str(e))
            data = self._get_local_cache(namespace)
            self._cache[namespace] = data

    def _long_poll(self) -> None:
        try:
            self._notification_map = self._get_namespaces()
            for namespace in self._notification_map.keys():
                if self.exceptNamespaces and namespace in self.exceptNamespaces:
                    continue
                self._get_config_by_namespace(namespace)
        except requests.exceptions.ReadTimeout as e:
            self.logger.warning(str(e))
        except requests.exceptions.ConnectionError as e:
            self.logger.warning(str(e))
            self._load_local_cache_file()

    def _load_local_cache_file(self) -> bool:
        """
        load all cached files from local path
        is only used while apollo server is unreachable
        :return:
        """
        try:
            for file_name in os.listdir(self._cache_file_path):
                file_path = os.path.join(self._cache_file_path, file_name)
                if os.path.isfile(file_path):
                    file_simple_name, file_ext_name = os.path.splitext(file_name)
                    if file_ext_name == ".swp":
                        continue
                    namespace = file_simple_name.split("_")[-1]
                    with open(file_path) as f:
                        self._cache[namespace] = json.loads(f.read())
            return True
        except Exception as e:
            self.logger.error(f"load local cache file error:{e}")
        return False

    def _listener(self) -> None:
        """

        :return:
        """
        while True:
            self.logger.debug("Entering listener loop...")
            self._long_poll()
            time.sleep(self._cycle_time)