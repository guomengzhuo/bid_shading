# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    : 
# @File    : read_data.py
# @Software: PyCharm

from data_process.read_market_price_data import ReadMarketPriceData
from data_process.read_impression_data import ReadImpressionPriceData
from data_process.rainbow_process import RainbowProcess
from configs.config import yky_dsp_redis_sample_conf, read_impression_last_hour
from configs.config import yky_dsp_rainbow_conf as rainbow_conf
from configs.config import rainbow_bid_shading_white_list_name
from configs.config import position_median_price_day_key, position_median_price_hour_key


class ReadData(object):
    """
    # 数据读取主类
    """

    def __init__(self, logging):
        """
        # 初始化
        """
        self.logging = logging

    def read_bid_shading_media_white_list(self):
        rainbow_env = "prod"
        ad_type_pro = RainbowProcess(rainbow_conf, rainbow_bid_shading_white_list_name, env=rainbow_env)
        is_ok, result = ad_type_pro.read_conf()

        media_white_list = []
        if not is_ok:
            self.logging.error(f"read RainbowProcess failed name:{rainbow_bid_shading_white_list_name}")
            return False, media_white_list

        self.logging.info(f"result:{result}")

        common_para = result["bid_shading_adjust_media_list"]
        if common_para == "":
            self.logging.error(f"read RainbowProcess bid_shading_adjust_media_list is empty")
            return False, media_white_list

        for media_id in common_para.split(","):
            media_white_list.append(int(media_id))

        self.logging.info(f"media_white_list:{media_white_list}")
        return True, set(media_white_list)

    def read_market_price_data(self):
        """
        read history market price from redis
        1、获取天级别的数据 market_price_day_dict
        2、获取小时级别的数据 market_price_hour_dict
        3、market_price_dict = market_price_hour_dict + （market_price_day_dict - market_price_hour_dict）

        """
        read_market_price_data = ReadMarketPriceData(self.logging, yky_dsp_redis_sample_conf)

        # 获取天级别的数据
        market_price_day_dict = read_market_price_data.read_from_redis(position_median_price_day_key)

        # 获取小时级别的数据
        market_price_hour_dict = read_market_price_data.read_from_redis(position_median_price_hour_key)

        # market_price_dict = market_price_hour_dict + （market_price_day_dict - market_price_hour_dict）
        market_price_dict = market_price_hour_dict
        # market_price_dict = {}
        # 优先取小时，天数据作为兜底
        for media_app_id, pos_info in market_price_day_dict.items():
            if media_app_id not in market_price_dict:
                market_price_dict[media_app_id] = pos_info
                self.logging.info(f"market_price_dict add media_app_id:{media_app_id}")

            for pos_id, pltv_info in pos_info.items():
                if pos_id not in market_price_dict[media_app_id]:
                    market_price_dict[media_app_id][pos_id] = pltv_info
                    self.logging.info(f"market_price_dict add media_app_id:{media_app_id}，pos_id:{pos_id}")

                for pltv, value in pltv_info.items():
                    if pltv not in market_price_dict[media_app_id][pos_id]:
                        market_price_dict[media_app_id][pos_id][pltv] = value
                        self.logging.info(f"market_price_dict add media_app_id:{media_app_id}，pos_id:{pos_id}, "
                                          f"pltv:{pltv}, value:{value}")

        self.logging.info(f"market_price_dict:{market_price_dict}")
        self.logging.info(f"len(market_price_dict):{len(market_price_dict)}, "
                          f"len(market_price_day_dict):{len(market_price_day_dict)}, "
                          f"len(market_price_hour_dict):{len(market_price_hour_dict)}")

        return market_price_dict

    def read_impression_price_data(self):
        """
        read real time impression pirce, last 1 hour
        """
        read_impression_price = ReadImpressionPriceData(self.logging, yky_dsp_redis_sample_conf)

        # 获取曝光数据
        impression_price_dict = read_impression_price.read_from_redis(is_impression=True,
                                                                      last_hour=read_impression_last_hour)
        self.logging.info(f"len(impression_price_dict):{len(impression_price_dict)}")

        # 获取响应未曝光数据
        no_impression_price_dict = read_impression_price.read_from_redis(is_impression=False,
                                                                         last_hour=read_impression_last_hour)
        self.logging.info(f"len(no_impression_price_dict):{len(no_impression_price_dict)}")

        return impression_price_dict, no_impression_price_dict

    def run(self):
        """
        main function
        """
        _, media_white_list = self.read_bid_shading_media_white_list()
        market_price_dict = self.read_market_price_data()
        impression_price_dict, no_impression_price_dict = self.read_impression_price_data()

        self.logging.info(f"len media_white_list:{len(media_white_list)},"
                          f"len market_price_dict:{len(market_price_dict)},"
                          f"len impression_price_dict:{len(impression_price_dict)},"
                          f"len no_impression_price_dict:{len(impression_price_dict)}")

        return media_white_list, market_price_dict, impression_price_dict, no_impression_price_dict


if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.run()
