# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm

import numpy as np
import pandas as pd
from configs.config import TEST_DATA_PATH
from data_process.read_data import ReadData


class ResultEvaluate(object):
    """
    # 数据读取主类
    """

    def __init__(self, logging):
        """
        # 初始化
        """
        self.logging = logging
        self.rd = ReadData(logging=self.logging, data_path=TEST_DATA_PATH)
        self.test_dataset = self.rd.test_data_process()

    def result_evaluation(self, result):
        # 读取测试数据集
        test_dataset = self.test_dataset
        evaluation = {}
        for media_app_id in result.keys():
            res = result[media_app_id]
            evaluation[media_app_id] = {}
            for key in res.keys():
                test_pd = test_dataset[test_dataset.key == key]
                result_dict = res[key]

                adjust_ratio_list = result_dict["adjust_ratio_list"]
                lower_bound = result_dict["lower_bound"]
                upper_bound = result_dict["upper_bound"]
                step = result_dict["step"]

                thresholds_linspace = np.arange(start=lower_bound, stop=upper_bound, step=step)

                test_pd = test_pd[(test_pd["virtual_ecpm"] < upper_bound) & (test_pd["virtual_ecpm"] > lower_bound)]
                bins = pd.cut(test_pd["virtual_ecpm"], bins=thresholds_linspace, labels=False)

                test_pd["bins"] = bins.map(int)
                index = test_pd["bins"].to_list()
                test_pd["adjust_ratio"] = [adjust_ratio_list[i] for i in index]

                test_pd["shading_ecpm"] = test_pd["virtual_ecpm"] * test_pd["adjust_ratio"]

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


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.data_process()
