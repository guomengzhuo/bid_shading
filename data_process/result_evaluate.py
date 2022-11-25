# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import os
import json
from datetime import datetime
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
            if test_pd.empty:
                self.logging.info(f"key:{key}, test_pd is empty!")
                continue

            # self.logging.info(f"key:{key}, test_pd:\n{test_pd.head()}")
            market_price = result_dict["market_price"]
            chosen_count_map = result_dict["chosen_count_map"]
            imp_count_map = result_dict["imp_count_map"]
            norm_dict = result_dict["norm_dict"]
            price, opt_gain, before_gain \
                = self.cal_price_adjustment_gain.get_adjust_price(test_pd[["response_ecpm", "win_price", "click_num",
                                                                           "target_cpa", "pay_amount"]],
                                                                  market_price, chosen_count_map,
                                                                  imp_count_map, norm_dict)

            # 二价数据集测试效果
            test_pd = test_pd.copy()
            test_pd["shading_ecpm"] = price
            test_pd["income"] = opt_gain
            test_pd["before_income"] = before_gain

            # 去掉未竞得的和数据异常的
            test_pd = test_pd[test_pd.target_price > 0]
            test_pd = test_pd[test_pd.target_price <= test_pd.response_ecpm]

            test_pd["label_before"] = np.select([
                (test_pd["response_ecpm"] >= test_pd["target_price"])],
                [test_pd["response_ecpm"]], default=0)
            """
            test_pd["label_increase"] = np.select([
                (test_pd["virtual_ecpm"] >= test_pd["target_price"])],
                [test_pd["virtual_ecpm"]], default=0)
            """
            test_pd["label_after"] = np.select([
                (test_pd["shading_ecpm"] >= test_pd["target_price"])],
                [test_pd["shading_ecpm"]], default=0)

            # 竞得率 & cpm
            win_rate_before = win_rate_after = 1.0
            cpm_after = 0
            if len(test_pd["label_before"]) != 0:
                win_rate_before = len(test_pd[test_pd["label_before"] > 0]) / len(test_pd["label_before"])
            cpm_before = sum(test_pd["label_before"]) / len(test_pd[test_pd["label_before"] > 0])

            if len(test_pd[test_pd["label_after"] > 0]):
                win_rate_after = len(test_pd[test_pd["label_after"] > 0]) / len(test_pd["label_after"])
                cpm_after = sum(test_pd["label_after"]) / len(test_pd[test_pd["label_after"] > 0])

            self.logging.info(f"key {key}, \n"
                              f"win rate before: {win_rate_before}, cpm before: {cpm_before} \n"
                              f"win rate after: {win_rate_after}, cpm after: {cpm_after}")

            evaluation[key] = {
                "win_rate_before": win_rate_before,
                "cpm_before": cpm_before,
                "win_rate_after": win_rate_after,
                "cpm_after": cpm_after
            }

        return evaluation

    def do_process(self, bandit_dict):

        # 步骤一、获取测试数据
        self.read_data()

        # 步骤二、评估结果
        evaluation_dict = self.result_evaluation(bandit_dict)

        result_dir = "./result"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        mhour = datetime.now().strftime("%Y%m%d%H")
        with open(result_dir + f"/evaluation_result_{mhour}.json", mode='w', encoding='utf-8') as f:
            json.dump(evaluation_dict, f)


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.data_process()
