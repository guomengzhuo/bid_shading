# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 10:22
# @Author  : biglongyuan
# @Site    : 
# @File    : search_optimal_price.py
# @Software: PyCharm

import collections

"""
从两个思路着手：
1、省钱的角度：max ∑(p(b*)(ecpm - b*))
2、挣钱的角度：调价后挣钱的钱要比没有调价挣得钱更多
max(∑(p(b*)(E(income) - b*)) - ∑(p(ecpm)(E(income) - ecpm)))
其中在给定 E(income)、ecpm条件下 ∑(p(ecpm)(E(income) - ecpm)) 是一个常数 记为 ecpm_income
max(∑(p(b*)(E(income) - b*)) - ecpm_income) -> max(∑(p(b*)(E(income) - b*)))
挑战 E(income)不好计算 同时 该种search方式 是和ecpm无关的

思考点：如果兼顾挣钱的同时考虑省钱因素



"""


def search_price_for_optimal_cost(logging, ecpm, market_price, upper_bound, chosen_count_map,
                                  imp_count_map, ecpm_norm_dict):
    """
    通过最大化∑win_rate * (ecpm-price), 找到最优出价点
    """
    ratio = 1.0
    gain = 0
    opt_price = 0
    win_rate_dict = {}
    for price, chosen_count in chosen_count_map.items():
        if chosen_count < 1 or price not in imp_count_map:
            continue

        imp_count = imp_count_map[price]

        # 最大化 impression_rate * (ecpm - price)
        price = ecpm_norm_dict[price]
        win_rate = imp_count * 1.0 / chosen_count
        win_rate_dict[price] = win_rate
        expect_gain = win_rate * (ecpm - price)
        if expect_gain > gain:
            gain = expect_gain
            ratio = price * 1.0 / ecpm
            opt_price = price

    ratio = round(ratio, 4)

    logging.info(f"market_price:{market_price}, opt_price:{opt_price}, ecpm:{ecpm}, ratio:{ratio}, gain:{gain},"
                 f" upper_bound:{upper_bound}, win_rate_dict:{win_rate_dict}")
    return ratio, gain


def search_price_for_optimal_income(logging, ecpm, market_price, upper_bound, chosen_count_map,
                                    imp_count_map, ecpm_norm_dict):
    """
    目标是最大化收益，income包括两部分 1、gmv; 2、本次出价节省的钱 (ecpm - price)
    通过最大化∑(win_rate * ROI) = ∑(win_rate * （gmv + ecpm - price）/price), 找到最优出价点
    其中 gmv = bid_price * win_rate
    """
    ratio = 1.0
    gain = 0
    opt_price = 0
    win_rate_dict = {}
    for price, chosen_count in chosen_count_map.items():
        if chosen_count < 1 or price not in imp_count_map:
            continue

        imp_count = imp_count_map[price]

        # 最大化 impression_rate * (ecpm - price)
        price = ecpm_norm_dict[price]
        win_rate = imp_count * 1.0 / chosen_count
        win_rate_dict[price] = win_rate
        expect_gain = win_rate * (ecpm - price)
        if expect_gain > gain:
            gain = expect_gain
            ratio = price * 1.0 / ecpm
            opt_price = price

    gain = max(0, price * (1 - ratio))
    ratio = round(ratio, 4)

    logging.info(f"market_price:{market_price}, opt_price:{opt_price}, ecpm:{ecpm}, ratio:{ratio}, gain:{gain},"
                 f" upper_bound:{upper_bound}, win_rate_dict:{win_rate_dict}")
    return ratio, gain
