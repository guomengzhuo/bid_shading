# -*- coding: utf-8 -*-
# @Time    : 2022/5/30 下午1:24
# @Author  : jaymizhang
# @Email   : jaymizhang@tencent.com
# @File    : rainbow_process.py
import sys
sys.path.append('../')

from rainbow_sdk.rainbow_client import RainbowClient


class RainbowProcess(object):
    def __init__(self, rainbow_conf, conf_name, env):
        """
        init configs
        :param rainbow_conf:
        :param env:
        """
        self.rainbow_conf = rainbow_conf
        self.conf_name = conf_name
        self.env = env

    def read_conf(self):
        rainbow_client = RainbowClient(self.rainbow_conf)
        result = rainbow_client.get_configs_v2(self.conf_name, env_name=self.env)
        if result["code"] != 0:
            return False, result["message"]

        return True, result["data"]
