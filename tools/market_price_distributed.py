# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 10:04
# @Author  : biglongyuan
# @Site    : 
# @File    : market_price_distributed.py
# @Software: PyCharm

import matplotlib.pyplot as plt


class Distributed_Image(object):
    """
    # 画图
    """
    def __init__(self, logging):
        """
        # 初始化
        """
        self.logging = logging
        
    def win_rate_image(self, market_price_value, imp_count_map, chosen_count_map, min_imp_price):
        win_rate = {
            i: imp_count_map[i] / chosen_count_map[i] for i in imp_count_map.keys()
        }

        for i in win_rate.keys():
            if i > market_price_value:
                _market_price_value = i
                break
        self.logging.info(f"market_price_value:{market_price_value}, _market_price_value:{_market_price_value}, "
                          f"min_imp_price:{min_imp_price}")
        fig = plt.figure(dpi=300)
        plt.scatter(win_rate.keys(), win_rate.values(), s=10)
        plt.scatter(_market_price_value, win_rate[_market_price_value], c="r", marker="^")
        if min_imp_price in win_rate:
            plt.scatter(min_imp_price, win_rate[min_imp_price], c="m", marker="*")

        plt.show()

    def true_history_win_rate(self, imp_count_map, chosen_count_map):
        win_rate = {
            i: imp_count_map[i] / chosen_count_map[i] for i in imp_count_map.keys()
        }

        fig = plt.figure(dpi=300)
        plt.scatter(win_rate.keys(), win_rate.values(), s=10)

        plt.show()

    def true_pred_win_rate(self, pred_imp_count_map, pred_chosen_count_map, true_imp_count_map, true_chosen_count_map,
                           market_price_value, min_imp_price):
        pred_win_rate = {
            i: pred_imp_count_map[i] / pred_chosen_count_map[i] for i in pred_imp_count_map.keys()
        }

        true_win_rate = {}
        acc_imp = 0
        acc_response = sum(true_chosen_count_map.values())
        for i in sorted(true_chosen_count_map.keys()):
            if i not in true_imp_count_map:
                true_win_rate[i] = acc_imp / (
                            acc_imp + true_chosen_count_map[i] + acc_response)
                acc_response -= true_chosen_count_map[i]
                continue
            true_win_rate[i] = (acc_imp + true_imp_count_map[i]) / (acc_imp + true_chosen_count_map[i] + acc_response)
            acc_imp += true_imp_count_map[i]
            acc_response -= true_chosen_count_map[i]

        for i in pred_win_rate.keys():
            if i >= market_price_value:
                _market_price_value = i
                break
        fig = plt.figure(dpi=300)
        # plt.title("{} distribution of game {}, date {}, user type{}".format())
        plt.scatter(pred_win_rate.keys(), pred_win_rate.values(), c='r', s=5, label="pred")
        plt.scatter(true_win_rate.keys(), true_win_rate.values(), c='blue', s=5, alpha=0.5, label='true')

        plt.scatter(_market_price_value, pred_win_rate[_market_price_value], c="green", marker="^")
        if min_imp_price in pred_win_rate:
            plt.scatter(min_imp_price, pred_win_rate[min_imp_price], c="green", marker="*")

        plt.legend()
        plt.show()

