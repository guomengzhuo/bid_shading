# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 10:22
# @Author  : biglongyuan
# @Site    : 
# @File    : search_optimal_price.py
# @Software: PyCharm

import collections


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

    gain = max(0, price * (1 - ratio))
    ratio = round(ratio, 4)

    logging.info(f"market_price:{market_price}, opt_price:{opt_price}, ecpm:{ecpm}, ratio:{ratio}, gain:{gain},"
                 f" upper_bound:{upper_bound}, win_rate_dict:{win_rate_dict}")
    return ratio, gain


def search_price_for_optimal_roi(ecpm, chosen_count_map, imp_count_map):
    """
    通过最大化∑(win_rate * ROI) = ∑(win_rate * E(payment)/price), 找到最优出价点
    """
    ratio = 0
    gain = 0

    for price, chosen_count in chosen_count_map.items():
        if chosen_count < 1 or ecpm not in imp_count_map:
            continue

        imp_count = imp_count_map[ecpm]

        # 最大化 impression_rate * (E(GMV) / price)
        expect_gain = (imp_count * 1.0 / chosen_count) * (ecpm / price)
        if expect_gain > gain:
            gain = expect_gain
            ratio = price * 1.0 / ecpm

    return ratio, gain
