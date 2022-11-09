# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:01
# @Author  : biglongyuan
# @Site    :
# @File    : bid_shading_e_e.py
# @Software: PyCharm


import os

from multiprocessing import Pool
import multiprocessing

import datetime
from data_process.read_data import ReadData
from data_process.result_evaluate import ResultEvaluate
from configs.config import DATA_PATH, TEST_DATA_PATH
from configs.config import PLTV_LEVEL, parallel_num, Environment
from bandit.UCB import UCBBandit
import logging
import numpy as np
import pandas as pd

if Environment == "offline":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )
else:
    logging.basicConfig(
        filename=os.path.join(os.getcwd(),
                              "./log/" + __file__.split(".")[0] + datetime.datetime.strftime(datetime.datetime.today(),
                                                                                             "_%Y%m%d") + ".log"),
        level=logging.INFO,
        filemode="a+",
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )


class BidShading(object):
    """
    bid shading 主类
    """

    def __init__(self, logging):
        """
        初始化
        """
        self.logging = logging

        # 价格数据初始化
        self.market_price_dict = {}
        self.impression_price_dict = {}
        self.media_position_dict = {}
        self.no_impression_price_dict = {}

        self.optimal_ratio_dict = {}

    def read_data(self, data_path=DATA_PATH):
        # 1、读取 bid shading输入数据
        rd = ReadData(logging=self.logging, data_path=data_path)

        # market_price_dict = media_app_id:position_id:pltv - value
        # impression_price_dict = media_app_id:position_id:pltv - value_list
        self.market_price_dict, self.impression_price_dict, self.no_impression_price_dict,\
            self.norm_dict = rd.data_process()

        self.logging.info(f"len market_price_dict:{len(self.market_price_dict)}, "
                          f"len impression_price_dict:{len(self.impression_price_dict)}")

        # 2、获取media、position映射关系
        for media_id, position_info in self.market_price_dict.items():

            if media_id not in self.media_position_dict:
                self.media_position_dict[media_id] = set(position_info.keys())
            else:
                self.media_position_dict[media_id] = self.media_position_dict[media_id] | set(position_info.keys())

        for media_id, position_info in self.impression_price_dict.items():

            if media_id not in self.media_position_dict:
                self.media_position_dict[media_id] = set(position_info.keys())
            else:
                self.media_position_dict[media_id] = self.media_position_dict[media_id] | set(position_info.keys())

        self.logging.info(f"media_position_dict:{self.media_position_dict}")

    def remove_local_backend(self):
        """
        删除临时文件
        :return:
        """
        return

    def run(self):
        self.logging.info("run -> start")

        bandit = UCBBandit()

        # 1、读取相关要处理的的数据
        self.read_data(DATA_PATH)

        re = ResultEvaluate(self.logging)

        res_l = {}  # 保存进程返回结果
        evaluate_l = {}
        for media_app_id in self.media_position_dict.keys():
            res = bandit.do_process(media_app_id, self.media_position_dict, self.market_price_dict,
                                    self.impression_price_dict, self.no_impression_price_dict)
            evaluate_l[res] = re.result_evaluation(res)
            res_l[media_app_id] = res

        # 2、计算并保存数据
        if Environment != "offline":
            pool = Pool(parallel_num)  # 构建进程池
            res_l = []  # 保存进程返回结果
            mgr = multiprocessing.Manager()
            media_position_dict_obj = mgr.dict(self.media_position_dict)
            market_price_dict_obj = mgr.dict(self.market_price_dict)
            impression_price_dict_obj = mgr.dict(self.impression_price_dict)
            no_impression_obj = mgr.dict(self.no_impression_price_dict)

            for media_app_id in self.media_position_dict.keys():
                res = pool.apply_async(bandit.do_process,
                                       args=(media_app_id, media_position_dict_obj, market_price_dict_obj,
                                             impression_price_dict_obj, no_impression_obj))
                res_l.append(res)

            pool.close()  # 关闭进程池，不再接受请求
            pool.join()  # 等待所有的子进程结束

            for res in res_l:
                self.logging.info(f"res:{res}")
                self.optimal_ratio_dict.update(res.get())

            pool.close()  # 关闭进程池，不再接受请求
            pool.join()  # 等待所有的子进程结束

            for res in res_l:
                self.logging.info(f"res:{res}")
                self.optimal_ratio_dict.update(res.get())
        else:
            for media_app_id in self.media_position_dict.keys():
                tmp_optimal_ratio_dict = bandit.do_process(media_app_id, self.media_position_dict,
                                                           self.market_price_dict,
                                                           self.impression_price_dict,
                                                           self.no_impression_price_dict)
                self.optimal_ratio_dict.update(tmp_optimal_ratio_dict)

        self.logging.info(f"run -> end len(optimal_ratio_dict):{len(self.optimal_ratio_dict)}")
        self.logging.info(f"output optimal_ratio_dict:{self.optimal_ratio_dict}")

        # 3、计算完 删除临时文件
        self.remove_local_backend()


def main():
    bs = BidShading(logging)
    bs.run()


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    main()
    