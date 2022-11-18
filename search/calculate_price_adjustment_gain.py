# -*- coding: utf-8 -*-
# @Time    : 2022/11/14 17:00
# @Author  : biglongyuan
# @Site    : 
# @File    : calculate_price_adjustment_gain.py
# @Software: PyCharm

from configs.config import ratio_step
from search.search_optimal_price import search_price_for_optimal_cost
import numpy as np


class calculate_price_adjustment_gain(object):
    """
    计算最优出价及收益
    """
    def __init__(self, logging):
        self.logging = logging

    def get_output_redis_adjust_ratio(self, media_app_id, position_id, level, impression_price_list,
                                      market_price_norm, chosen_count_map, imp_count_map, ecpm_norm_dict,
                                      optimal_ratio_dict):
        """
        设置市场价格调整比例
        """

        market_price = 0.0
        if market_price_norm in ecpm_norm_dict:
            market_price = ecpm_norm_dict[market_price_norm]

        upper_bound = int(1.5 * market_price)
        if len(impression_price_list) > 1:
            max_imp_price = ecpm_norm_dict[impression_price_list[-1]]
            upper_bound = int(max(max_imp_price * 1.1, 1.5 * market_price))

        lower_bound = int(market_price * 0.9)
        step = ratio_step

        if level == -1:
            key = f"{media_app_id}_{position_id}"
        else:
            key = f"{media_app_id}_{position_id}_{level}"

        if key not in optimal_ratio_dict:
            optimal_ratio_dict[key] = {}

        # todo(@mfishzhang): 修改
        # ecpm_list = np.arange(lower_bound, upper_bound, step)
        ecpm_list = np.arange(lower_bound, upper_bound, step)
        adjust_ratio = []
        gain_list = []
        for price in ecpm_list:
            if price <= market_price:
                adjust_ratio.append(1.0)
            else:
                assert upper_bound - market_price > 0
                y, gain = search_price_for_optimal_cost(logging, price, market_price, upper_bound, chosen_count_map,
                                                        imp_count_map, ecpm_norm_dict)
                adjust_ratio.append(y)
                gain_list.append(gain)

        optimal_ratio_dict[key]['adjust_ratio_list'] = adjust_ratio
        optimal_ratio_dict[key]['upper_bound'] = upper_bound
        optimal_ratio_dict[key]['lower_bound'] = lower_bound
        optimal_ratio_dict[key]['step'] = step
        optimal_ratio_dict[key]['avg_income'] = sum(gain_list) / len(gain_list)
        optimal_ratio_dict[key]['sum_income'] = sum(gain_list)
        self.logging.info(f"key:{key}, upper_bound:{upper_bound}, lower_bound:{lower_bound}, "
                          f"market_price:{market_price}, sum_income:{sum(gain_list)}, "
                          f"avg_income:{sum(gain_list) / len(gain_list)}")

    def get_adjust_price(self, ecpm_pd, market_price, chosen_count_map, imp_count_map, norm_dict):
        """
        给定ecpm，计算最优出价
        """

        norm_max = norm_dict["norm_max"]
        norm_min = norm_dict["norm_min"]
        price_list = []
        gain_list = []
        # self.logging.info(f"ecpm_pd:\n{ecpm_pd.head()}")
        for index, ecpm_meta in ecpm_pd.iterrows():
            ecpm = ecpm_meta["response_ecpm"]
            win_price = ecpm_meta["win_price"]
            click_num = ecpm_meta["click_num"]
            target_cpa = ecpm_meta["target_cpa"]
            pay_amount = ecpm_meta["pay_amount"]
            ecpm = ecpm * (norm_max - norm_min) + norm_min
            price, gain = search_price_for_optimal_cost(self.logging, ecpm, market_price,
                                                        chosen_count_map, imp_count_map, norm_dict)
            self.logging.info(f"ecpm:{ecpm}, price:{price}, gain:{gain}, win_price:{win_price}, click_num:{click_num}, "
                              f"target_cpa:{target_cpa}, pay_amount:{pay_amount}")
            price_list.append(price)
            gain_list.append(gain)

        return price_list, gain_list

    def test_data_find_optimization_gain(self, media_app_id, position_id, level, impression_price_list,
                                         market_price_norm, chosen_count_map, imp_count_map,
                                         ecpm_norm_dict, optimal_ratio_dict):
        """
        设置市场价格调整比例
        """

        market_price = 0.0
        if market_price_norm in ecpm_norm_dict:
            market_price = ecpm_norm_dict[market_price_norm]

        upper_bound = int(1.5 * market_price)
        if len(impression_price_list) > 1:
            max_imp_price = ecpm_norm_dict[impression_price_list[-1]]
            upper_bound = int(max(max_imp_price * 1.1, 1.5 * market_price))

        lower_bound = int(market_price * 0.9)
        step = ratio_step

        if level == -1:
            key = f"{media_app_id}_{position_id}"
        else:
            key = f"{media_app_id}_{position_id}_{level}"

        if key not in optimal_ratio_dict:
            optimal_ratio_dict[key] = {}

        # todo(@mfishzhang): 修改
        # ecpm_list = np.arange(lower_bound, upper_bound, step)
        ecpm_list = np.arange(lower_bound, upper_bound, step)
        adjust_ratio = []
        gain_list = []
        for price in ecpm_list:
            if price <= market_price:
                adjust_ratio.append(1.0)
            else:
                assert upper_bound - market_price > 0
                y, gain = search_price_for_optimal_cost(logging, price, market_price, upper_bound, chosen_count_map,
                                                        imp_count_map, ecpm_norm_dict)
                adjust_ratio.append(y)
                gain_list.append(gain)

        optimal_ratio_dict[key]['adjust_ratio_list'] = adjust_ratio
        optimal_ratio_dict[key]['upper_bound'] = upper_bound
        optimal_ratio_dict[key]['lower_bound'] = lower_bound
        optimal_ratio_dict[key]['step'] = step
        optimal_ratio_dict[key]['avg_income'] = sum(gain_list) / len(gain_list)
        optimal_ratio_dict[key]['sum_income'] = sum(gain_list)
        logging.info(f"key:{key}, upper_bound:{upper_bound}, lower_bound:{lower_bound}, market_price:{market_price}, "
                     f"sum_income:{sum(gain_list)}, avg_income:{sum(gain_list) / len(gain_list)}")
