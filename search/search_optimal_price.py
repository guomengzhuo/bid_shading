# -*- coding: utf-8 -*-
# @Time    : 2022/11/11 10:22
# @Author  : biglongyuan
# @Site    : 
# @File    : search_optimal_price.py
# @Software: PyCharm


def search_price_for_optimal_cost(logging, ecpm, market_price, upper_bound, chosen_count_map,
                                  imp_count_map, ecpm_norm_dict):
    ratio = 1.0
    gain = 0
    opt_price = 0
    for price, chosen_count in chosen_count_map.items():
        if chosen_count < 1 or price not in imp_count_map:
            continue

        imp_count = imp_count_map[price]

        # 最大化 impression_rate * (ecpm - price)
        price = ecpm_norm_dict[price]
        expect_gain = (imp_count * 1.0 / chosen_count) * (ecpm - price)
        if expect_gain > gain:
            gain = expect_gain
            ratio = price * 1.0 / ecpm
            opt_price = price

    if ratio == 1.0:
        # 等比例缩小
        ratio = ((ecpm - market_price) * (market_price * 1.5 - market_price) /
                 (upper_bound - market_price) + market_price) / ecpm

    gain = max(0, price * (1 - ratio))
    ratio = round(ratio, 4)

    # logging.info(f"market_price:{market_price}, opt_price:{opt_price}, ecpm:{ecpm}, ratio:{ratio}, gain:{gain},"
    #              f" upper_bound:{upper_bound}")
    return ratio, gain


def search_price_for_optimal_roi(ecpm, chosen_count_map, imp_count_map):
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
