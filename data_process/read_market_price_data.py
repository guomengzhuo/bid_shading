# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:13
# @Author  : biglongyuan
# @Site    : 
# @File    : read_market_price_data.py
# @Software: PyCharm

import redis
import os
import json


class ReadMarketPriceData(object):
    """
    # 获取媒体市场价格
    """

    def __init__(self, logging, redis_conf, env="prob"):
        self.logging = logging
        self.redis_conf = redis_conf
        self.env = env

    def write_data_to_local(self, data_dict, redis_prefix_key):
        if not os.path.exists(f"{os.getcwd()}/data"):
            os.makedirs(f"{os.getcwd()}/data")
            self.logging.info(f"makedirs {os.getcwd()}/data")

        file_name = f"{os.getcwd()}/data/{redis_prefix_key}.json"
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                json.dump(data_dict, f)
                self.logging.info(f"write json data complete ./data/{redis_prefix_key}.json")
        else:
            self.logging.info(f"{file_name} is exist")

    def get_local_data(self, redis_key):

        data_dict = {}
        file_path = f"{os.getcwd()}/data/{redis_key}.json"

        if not os.path.exists(file_path):
            return False, data_dict

        with open(file_path, 'r') as fr:
            self.logging.info(f"open {file_path}")
            data_dict = json.loads(fr.read())
            self.logging.info(f"len data_dict:{len(data_dict)}")

        return True, data_dict

    def get_data(self, redis_key):
        """
        read from redis, first priority
        """
        output_dict = {}

        if self.env == "offline":
            output_dict = self.get_local_data(redis_key)
            return output_dict

        redis_client = redis.Redis(host=self.redis_conf["host"],
                                   port=self.redis_conf["port"],
                                   password=self.redis_conf["auth"])
        res = redis_client.hgetall(redis_key)

        if len(res) < 1:
            self.logging.info(f"redis_key:{redis_key} is empty!")
            return output_dict

        # self.logging.info(f"res:{res}")
        for key, value in res.items():
            # key = mediaAppId_position_id_pltvLevel
            # value = win_price 千次曝光分
            key = key.decode().strip().split("_")
            if len(key) != 3:
                continue

            media_app_id = int(key[0])
            position_id = int(key[1])
            pltv = int(key[2])
            # self.logging.info(f"---media_app_id:{media_app_id}, position_id:{position_id},"
            #                   f" pltv:{pltv}, value:{int(value)}")

            if media_app_id not in output_dict:
                output_dict[media_app_id] = {}

            position_dict = output_dict[media_app_id]
            if position_id not in position_dict:
                position_dict[position_id] = {}

            pltv_dict = position_dict[position_id]
            if pltv not in pltv_dict:
                pltv_dict[pltv] = 0

            pltv_dict[pltv] = int(value)
            position_dict[position_id] = pltv_dict
            output_dict[media_app_id] = position_dict

        # 将数据本地化存储
        self.write_data_to_local(output_dict, redis_key)

        # self.logging.info(f"---output_dict:{output_dict}")
        return output_dict


if __name__ == '__main__':
    import logging
    from configs.config import yky_dsp_redis_sample_conf, position_median_price_hour_key

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadMarketPriceData(logging, yky_dsp_redis_sample_conf)
    rd.get_data(position_median_price_hour_key)
