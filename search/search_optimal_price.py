# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 10:22
# @Author  : biglongyuan
# @Site    : 
# @File    : search_optimal_price.py
# @Software: PyCharm


def search_price_for_optimal_cost(ecpm, chosen_count_map, imp_count_map):
    ratio = 0
    gain = 0

    for price, chosen_count in chosen_count_map.items():
        if chosen_count < 1 or ecpm not in imp_count_map:
            continue

        imp_count = imp_count_map[ecpm]

        # 最大化 impression_rate * (ecpm - price)
        expect_gain = (imp_count * 1.0 / chosen_count) * (ecpm - price)
        if expect_gain > gain:
            gain = expect_gain
            ratio = price * 1.0 / ecpm

    return ratio

