# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:13
# @Author  : biglongyuan
# @Site    : 
# @File    : read_market_price_data.py
# @Software: PyCharm

import redis


class ReadMarketPriceData(object):
    """
    # 获取媒体市场价格
    """

    def __init__(self, logging, redis_conf):
        self.logging = logging
        self.redis_conf = redis_conf

    def read_from_redis(self, redis_key):
        """
        read from redis, first priority
        """
        output_dict = {}
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
    rd.read_from_redis(position_median_price_hour_key)
