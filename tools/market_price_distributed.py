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
        
    def win_rate_image(self, market_price_value, imp_count_map, chosen_count_map):
        win_rate = {
            i: imp_count_map[i] / chosen_count_map[i] for i in imp_count_map.keys()
        }

        for i in win_rate.keys():
            if i > market_price_value:
                _market_price_value = i
                break
        fig = plt.figure(dpi=300)
        plt.scatter(win_rate.keys(), win_rate.values(), s=10)
        plt.scatter(_market_price_value, win_rate[_market_price_value], c="r")

        plt.show()