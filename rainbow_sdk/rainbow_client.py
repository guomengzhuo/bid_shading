#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : rainbow_client.py
# Author            : joshzyjian <joshzyjian@tencent.com>
# Date              : 28.06.2020
# Last Modified Date: 28.06.2020
# Last Modified By  : joshzyjian <joshzyjian@tencent.com>
# coding: utf-8

import json
import re
import time
import threading
from rainbow_sdk.http import HttpClient
from rainbow_sdk.utils import get_route, get_local_host_ip
from rainbow_sdk.cache import FileCache, MemCache

REG_IP_AND_PORT = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{3,5}$"
REG_URL = r"^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?:8080$"
REG_L5 = r"^\d{3,10}\:\d{3,10}$"
LONG_LOOP_TIME = 10


class RainbowClient(object):
    """rainbow客户端同步SDK ."""

    def __init__(self, init_config):
        """初始化 .

        Args:
            connectStr(string): 项目ID：通过申请签名账号页面获取
            isUsingLocalCache(bool): 授权用户ID：通过申请签名账号页面获取
            isUsingFileCache(string): 授权密钥
            isConnectLocalAgent(string): 项目ID：通过申请签名账号页面获取
            connectLocalPort(string): 授权用户ID：通过申请签名账号页面获取
            protocolVersion(string): 协议版本：v1; v2;
            tokenConfig(dict): 授权 信息
            tokenConfig[app_id](string): 项目ID：通过申请签名账号页面获取
            tokenConfig[user_id](string): 授权用户ID：通过申请签名账号页面获取
            tokenConfig[secret_key](string): 授权密钥
            client_infos(list): 自定义客户端标识
            client_infos[i][clientIdentifiedName]: 标识键
            client_infos[i][clientIdentifiedValue]: 标识值
        """

        self.connect_str = init_config.get('connectStr', '')
        self.is_using_local_cache = init_config.get('isUsingLocalCache', False)
        self.is_using_file_cache = init_config.get('isUsingFileCache', False)
        self.is_connect_local_agent = init_config.get('isConnectLocalAgent', False)
        self.connect_local_port = init_config.get('connectLocalPort', 0)
        self.file_cache_path = init_config.get('fileCachePath', '')
        self.long_loop_time = init_config.get('longLoopTime', LONG_LOOP_TIME)
        self.local_network_card = init_config.get('localNetworkCard', 'eth1')

        # 获取协议版本
        self.protocol_version = init_config.get('protocolVersion', "v2")
        # 判断最后一位是否是/
        if self.file_cache_path and not (self.file_cache_path[:-1] == "/"):
            self.file_cache_path += "/"

        if not self.file_cache_path:
            self.is_using_file_cache = False
        token_config = init_config.get('tokenConfig', {})
        self.app_id = token_config.get("app_id", "")
        self.user_id = token_config.get("user_id", "")
        self.secret_key = token_config.get("secret_key", "")

        self.connect_host_str = self.get_connect_host_str()

        self.client_infos = init_config.get('client_infos', [])

    def get_connect_host_str(self):
        # 是否安装本机agent
        if self.is_connect_local_agent:
            # 按照真实的部署端口来填写
            self.connect_host_str = "127.0.0.1:%s" % self.connect_local_port
        else:
            if self.connect_str:
                if re.match(REG_IP_AND_PORT, self.connect_str):
                    # 匹配上是IP+Port
                    self.connect_host_str = self.connect_str
                elif re.match(REG_URL, self.connect_str):
                    # 匹配上是Url
                    self.connect_host_str = self.connect_str
                elif re.match(REG_L5, self.connect_str):
                    # 匹配上是L5
                    l5_list = self.connect_str.split(":")
                    if l5_list:
                        ip, port = get_route(int(l5_list[0]), int(l5_list[1]))
                        self.connect_host_str = "%s:%d" % (ip, port)
                else:
                    # 其他情况默认用户填写为请求地址
                    self.connect_host_str = self.connect_str
            else:
                self.connect_host_str = ""
        return self.connect_host_str

    def get_configs(self, group, version="", key="", env_name="", start=None, offset=None):
        # 兼容旧版数据结构接口
        config_res = self.get_configs_v2(group, version, key, env_name, start, offset)
        if config_res["code"] == 0:
            return config_res["data"]
        else:
            return False

    def get_configs_v2(self, group, version="", key="", env_name="", start=None, offset=None):
        pull_item = self.make_pull_item(group, version, key, env_name, start, offset)

        # 判断是否从文件缓存拉取数据
        if self.is_using_file_cache:
            cache_client = FileCache(
                {"pull_item": pull_item, "fileCachePath": self.file_cache_path}
            )
            config_values = cache_client.get()
            if config_values:
                return {
                    "code": 0,
                    "data": config_values,
                    "message": "OK"
                }

        # 判断是否从本地缓存拉取数据
        if self.is_using_local_cache:
            cache_client = MemCache({"pull_item": pull_item, })
            config_values = cache_client.get()
            if config_values:
                return {
                    "code": 0,
                    "data": config_values,
                    "message": "OK"
                }

        http_client = HttpClient(
            self.connect_host_str, self.app_id, self.user_id, self.secret_key, self.protocol_version
        )

        # 组装获取配置请求接口参数
        local_ip = get_local_host_ip(str.encode(self.local_network_card))
        client_infos = list()
        client_infos.append(
            {"clientIdentifiedName": "ip", "clientIdentifiedValue": local_ip}
        )
        client_infos.extend(self.client_infos)

        res = http_client.pull_config_req(client_infos, pull_item)
        if res and "ret_code" in res and int(res["ret_code"]) == 0:
            # 解析一下数据结构，目前只考虑KV数据结构
            data = dict()
            if res["config"]["items"]:
                for item in res["config"]["items"]:
                    if item["struct_type"] == 0:
                        # KV结构
                        for key_value in item["key_values"]:
                            data[key_value["key"]] = key_value["value"]
                    elif item["struct_type"] == 1:
                        # Table结构
                        table_data = [json.loads(i) for i in item["rows"]]
                        data = {
                            "rows": table_data,
                            "rows_end": item["rows_end"]
                        }
            # 调用请求成功, 缓存数据
            if self.is_using_file_cache or self.is_using_local_cache:
                # 版本缓存
                cache_client.set(data)
                # 最新版本，不需要存储，因为polling长轮询将重新初始化
            if self.is_using_local_cache:
                cache_client.set(data)

            return {
                "code": 0,
                "data": data,
                "message": "OK"
            }
        else:
            return {
                "code": -1,
                "data": {},
                "message": res["ret_msg"]
            }

    def make_pull_item(self, group, version="", key="", env_name="", start=None, offset=None):
        pull_item = {"app_id": self.app_id, "group": group}
        if version:
            pull_item["version"] = version
        if key:
            pull_item["key"] = key
        if env_name:
            pull_item["env_name"] = env_name
        if start is not None:
            pull_item["start"] = start
        if offset is not None:
            pull_item["offset"] = offset

        return pull_item

    def pulling_req(self, group, version="", key="", env_name=""):
        http_client = HttpClient(
            self.connect_host_str, self.app_id, self.user_id, self.secret_key, self.protocol_version
        )

        # 组装获取配置请求接口参数
        local_ip = get_local_host_ip(str.encode(self.local_network_card))
        client_infos = list()
        client_infos.append(
            {"clientIdentifiedName": "ip", "clientIdentifiedValue": local_ip}
        )
        client_infos.extend(self.client_infos)
        pull_item = self.make_pull_item(group, version, key, env_name)

        res = http_client.pulling_req(client_infos, pull_item)
        if res and "ret_code" in res and int(res["ret_code"]) == 0:
            return {
                "code": 0,
                "data": res["config"],
                "message": "OK"
            }
        else:
            return {
                "code": -1,
                "data": {},
                "message": res["ret_msg"]
            }

    def default_polling_worker(self, group, version="", key="", env_name="", callback=None):
        def default_callback(pull_item, response):
            if self.is_using_file_cache:
                if not response:
                    return
                # 先获取已缓存的文件数据
                cache_client = FileCache(
                    {"pull_item": pull_item, "fileCachePath": self.file_cache_path}
                )
                data = cache_client.get()
                for item in response["items"]:
                    """
                    NONE = 0;
                    UPDATE = 1; // 表示更新的key
                    ADD = 2; // 表示添加的key
                    DELETE = 3; // 表示删除的key
                    ALL = 4; // 表示全量覆盖
                  """
                    if (self.protocol_version == "v1" and item["event_type"] == "UPDATE") or item["event_type"] == 1:
                        for key_value in item["key_values"]:
                            data[key_value["key"]] = key_value["value"]
                    elif (self.protocol_version == "v1" and item["event_type"] == "ADD") or item["event_type"] == 2:
                        for key_value in item["key_values"]:
                            data[key_value["key"]] = key_value["value"]
                    elif (self.protocol_version == "v1" and item["event_type"] == "DELETE") or item["event_type"] == 3:
                        for key_value in item["key_values"]:
                            del data[key_value["key"]]
                    elif (self.protocol_version == "v1" and item["event_type"] == "ALL") or item["event_type"] == 4:
                        # 重新组装数据
                        data = dict()
                        for key_value in item["key_values"]:
                            data[key_value["key"]] = key_value["value"]
                # 将完整数据更新到本地缓存
                cache_client.set(data)

        local_version = version
        while True:
            response = self.pulling_req(group, local_version, key, env_name)
            if response and response["code"] != 0:
                continue
            response = response['data']
            pull_item = self.make_pull_item(group, local_version, key, env_name)
            if response:
                if callback:
                    callback(response)
                else:
                    default_callback(pull_item, response)
            if response and response["items"] and response["items"][0]["version"]:
                local_version = response["items"][0]["version"]
            time.sleep(self.long_loop_time)

    def add_listener(self, group, version="", key="", env_name="", callback=None):
        # 定义默认修改缓存文件数据
        t = threading.Thread(
            target=self.default_polling_worker, args=(group, version, key, env_name, callback,))
        # 主线程结束时，子线程也随之结束
        t.setDaemon(True)
        t.start()

    def get_kv_configs(self, group, version="", key="", env_name=""):
        configs = self.get_configs(group, version, key, env_name)
        return configs

    def get_table_configs(self, group, version="", key="", env_name="", start=None, offset=None):
        configs = self.get_configs(group, version, key, env_name, start, offset)
        return configs
