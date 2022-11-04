# coding: utf-8

import requests
import json
from rainbow_sdk.auth import Signature
from rainbow_sdk.utils import logger


class HttpClient(object):
    """API签名校验客户端类库 ."""

    def __init__(self, request_host, app_id, user_id, secret_key, protocol_version):
        """初始化 .

        Args:
            app_id(string): 项目ID：通过申请签名账号页面获取
            user_id(string): 授权用户ID：通过申请签名账号页面获取
            secret_key(string): 授权密钥
            request_host(string): 初始化请求地址Host
        """
        self.auth = Signature(app_id, user_id, secret_key)
        if not request_host.startswith("http"):
            self.request_host = "http://" + request_host
        else:
            self.request_host = request_host
        self.protocol_version = protocol_version

    def pull_config_req(self, client_infos, pull_item):
        headers = self.auth.get_client_header()
        # 需要指定协议为json
        headers["Content-Type"] = "application/json"

        # 组装获取配置请求接口参数
        config_req_params = {"client_infos": client_infos, "pull_item": pull_item}

        post_url = self.request_host + "/config.v2.ConfigService/PullConfigReq"
        if self.protocol_version == "v1":
            post_url = self.request_host + "/config.ConfigService/PullConfigReq"
        res = requests.post(
            post_url,
            headers=headers,
            data=json.dumps(config_req_params).encode("utf-8"),
            timeout=5,
        )
        if res.status_code == 200:
            # 调用请求成功
            return json.loads(res.text)
        else:
            logger.info(res.text)
            return False

    def pulling_req(self, client_infos, pull_item):
        headers = self.auth.get_client_header()
        # 需要指定协议为json
        headers["Content-Type"] = "application/json"
        headers["Connection"] = "keep-alive"

        # 组装获取配置请求接口参数
        config_req_params = {"client_infos": client_infos, "polling_item": pull_item}
        post_url = self.request_host + "/config.v2.ConfigService/PollingReq"
        if self.protocol_version == "v1":
            post_url = self.request_host + "/config.ConfigService/PollingReq"
        res = requests.post(
            post_url,
            headers=headers,
            data=json.dumps(config_req_params).encode("utf-8"),
            timeout=120,
            stream=True,
        )
        if res.status_code == 200:
            # 调用请求成功
            return json.loads(res.text)
        else:
            logger.info(res.text)
            return False
