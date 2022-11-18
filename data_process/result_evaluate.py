# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm

import numpy as np
import pandas as pd
from configs.config import TEST_DATA_PATH, No_pltv, ratio_step
from data_process.read_data import ReadData
from search.calculate_price_adjustment_gain import calculate_price_adjustment_gain


class ResultEvaluate(object):
    """
    # 数据读取主类
    """

    def __init__(self, logging):
        """
        # 初始化
        """
        self.logging = logging
        self.data_list = []
        self.cal_price_adjustment_gain = calculate_price_adjustment_gain(self.logging)

    def read_data(self):
        read_data = ReadData(logging=self.logging, data_path=TEST_DATA_PATH)
        self.data_list = read_data.test_data_process()

    def analyze_bandit_dict(self, bandit_dict):
        bandit_result = {}
        for key, optimal_ratio_dict in bandit_dict.items():
            key_list = key.split("_")
            media_app_id = key_list[0]
            position_id = key_list[1]
            if media_app_id not in bandit_result:
                bandit_result[media_app_id] = {}

            if No_pltv:
                bandit_result[media_app_id][position_id] = optimal_ratio_dict
            else:
                pltv_level = -1
                if not No_pltv and len(key_list) == 3:
                    pltv_level = key_list[2]

                position_dict = bandit_dict[media_app_id]
                if position_id not in position_dict:
                    position_dict[position_id] = {}

                position_dict[pltv_level] = optimal_ratio_dict
                bandit_result[media_app_id][position_id] = position_dict

        return bandit_result

    def result_evaluation(self, result):
        """
        评估search
        """
        evaluation = {}
        self.logging.info(f"result.keys():{result.keys()}\n"
                          f"test_dataset:{self.data_list.head(100)}")

        for key, result_dict in result.items():
            test_pd = self.data_list[self.data_list.key == key]
            market_price = result_dict["market_price"]
            price, gain = self.cal_price_adjustment_gain.get_adjust_price(test_pd["response_ecpm"], market_price,
                                                                          chosen_count_map,
                                                                          imp_count_map, norm_dict)

            test_pd["shading_ecpm"] = price
            test_pd["income"] = gain
            test_pd["label_before"] = np.select([
                (test_pd["response_ecpm"] >= test_pd["target_price"])],
                [test_pd["response_ecpm"]], default=0)

            test_pd["label_increase"] = np.select([
                (test_pd["virtual_ecpm"] >= test_pd["target_price"])],
                [test_pd["virtual_ecpm"]], default=0)

            test_pd["label_after"] = np.select([
                (test_pd["shading_ecpm"] >= test_pd["target_price"])],
                [test_pd["shading_ecpm"]], default=0)

            # 竞得率 & cpm
            win_rate_before = 1.0
            if len(test_pd["label_before"]) != 0:
                win_rate_before = len(test_pd[test_pd["label_before"] > 0]) / len(test_pd["label_before"])

            cpm_before = sum(test_pd["label_before"]) / len(test_pd[test_pd["label_before"] > 0])

            win_rate_increase = len(test_pd[test_pd["label_increase"] > 0]) / len(test_pd["label_increase"])
            cpm_increase = sum(test_pd["label_increase"]) / len(test_pd[test_pd["label_increase"] > 0])

            win_rate_after = len(test_pd[test_pd["label_after"] > 0]) / len(test_pd["label_after"])
            cpm_after = sum(test_pd["label_after"]) / len(test_pd[test_pd["label_after"] > 0])

            self.logging.info(f"key {key}, \n"
                              f"win rate before: {win_rate_before}, cpm before: {cpm_before} \n"
                              f"win rate increase: {win_rate_increase}, cpm after: {cpm_increase} \n"
                              f"win rate after: {win_rate_after}, cpm after: {cpm_after}")

            evaluation[media_app_id][key] = {
                "win_rate_before"
            }

        return evaluation

    def do_process(self, bandit_dict):

        # 步骤一、获取测试数据
        self.read_data()

        # 步骤二、评估结果
        self.result_evaluation(bandit_dict)


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.data_process()
