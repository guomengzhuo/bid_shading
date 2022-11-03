# -*- coding: utf-8 -*-
# @Time    : 2022/10/09 17:51
# @Author  : biglongyuan
# @Site    :
# @File    : redis_process.py
# @Software: PyCharm

import redis
import time
import json
from data_process.zip_compress import zip_2_string, string_2_zip


class RedisProcess(object):
    """
    redis process
    """

    def __init__(self, logging, redis_conf, env):
        """ init redis client"""
        self.logging = logging
        self.MAX_RETRY_TIMES = 3
        self.client = redis.Redis(
            host=redis_conf[env]["host"],
            port=redis_conf[env]["port"],
            password=redis_conf[env]["auth"]
        )

    def close(self):
        """
        close client()
        :return: None
        """
        self.client.close()

    def write_redis(self, key, data, is_zip=False, timeout=7 * 24 * 3600):
        """
        write data to redis with zip
        :param key:
        :param data:
        :param is_zip:
        :param timeout:
        :return:
        """

        data_json = json.dumps(data)
        if is_zip:
            data_json = string_2_zip(data_json)

        for i in range(self.MAX_RETRY_TIMES):
            try:
                self.client.set(key, data_json)
                self.client.expire(key, timeout)
                self.logging.info(f'[success] write {key} to redis  ]')
                return True
            except redis.exceptions as ex:
                self.logging.info(f"[failed] write {key} to redis  ] " + ex)
                time.sleep(5)
                continue
            finally:
                pass
        return False