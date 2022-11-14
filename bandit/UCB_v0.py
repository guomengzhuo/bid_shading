# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 11:38
# @Author  : biglongyuan, mfishzhang
# @Site    : 
# @File    : UCB.py
# @Software: PyCharm

import logging
import math
import multiprocessing
import numpy as np
from configs.config import PLTV_LEVEL, max_search_num, ratio_step, Environment
from tools.market_price_distributed import Distributed_Image
from search.get_adjust_ratio import get_adjust_ratio
import copy

if Environment == "offline":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )
else:
    logging.basicConfig(
        filename=os.path.join(os.getcwd(),
                              "./log/" + __file__.split(".")[0] + datetime.datetime.strftime(datetime.datetime.today(),
                                                                                             "_%Y%m%d") + ".log"),
        level=logging.INFO,
        filemode="a+",
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )


class UCBBandit(object):
    """
    bid shading 主类
    """

    def __init__(self):
        """
        初始化
        """

    def calculate_market_price(self, media_app_id, position_id, market_price_dict,
                               impression_price_dict, no_impression_price, ecpm_norm_dict, optimal_ratio_dict):
        """
        计算市场价格
        :params market_price_dict = {pltv:value}
        :params impression_price_dict = {pltv:value_list}
        :params no_impression_price = {pltv:value_list}  响应未曝光数据
        """
        # """分pltv计算"""
        for level in PLTV_LEVEL:
            market_price_value = -1.0
            impression_price_list = []
            no_impression_price_list = []
            if level in market_price_dict:
                market_price_value = market_price_dict[level]

            if level in impression_price_dict:
                impression_price_list = sorted(impression_price_dict[level], reverse=False)

            if level in no_impression_price:
                no_impression_price_list = sorted(no_impression_price[level], reverse=False)

            if market_price_value == -1.0 or len(impression_price_list) < 100:
                # TODO market_price_value 使用的媒体回传数据，要限制大小？
                logging.debug(f"proc_id={multiprocessing.current_process().name},"
                              f"media_app_id:{media_app_id}, position_id:{position_id}, level:{level},"
                              f"len(impression_price_list):{len(impression_price_list)} < 10, data is sparse "
                              f"enough to compute")
                continue

            # e-e
            # market_price 市场价格
            # chosen_count_map = {}  # 记录选择次数
            # imp_count_map = {}  # 记录曝光次数
            market_price, chosen_count_map, imp_count_map = self.bandit(market_price_value,
                                                                        impression_price_list,
                                                                        no_impression_price_list)

            logging.info(f"proc_id={multiprocessing.current_process().name},"
                         f"media_app_id:{media_app_id}, position_id:{position_id}, level:{level}, "
                         f"history_median_price_value:{market_price_value}, market_price:{market_price}，"
                         f"len impression_price_list:{len(impression_price_list)}, "
                         f"len no_impression_price_list:{len(no_impression_price_list)}")

            # 设置市场价格调整比例
            get_adjust_ratio(logging, media_app_id, position_id, level, impression_price_list,
                             market_price, chosen_count_map, imp_count_map, ecpm_norm_dict, optimal_ratio_dict)

        # """计算position默认值 """
        market_price_value = -1.0
        market_price_value_list = []
        impression_price_list = []
        no_impression_price_list = []

        for value in market_price_dict.values():
            market_price_value_list.append(value)

        if len(market_price_value_list) > 0:
            market_price_value = round(np.mean(market_price_value_list), 2)

        for value in impression_price_dict.values():
            impression_price_list += value

        impression_price_list = sorted(impression_price_list, reverse=False)

        for value in no_impression_price.values():
            no_impression_price_list += value

        no_impression_price_list = sorted(no_impression_price_list, reverse=False)

        if market_price_value == -1.0 or len(impression_price_list) < 100:
            # TODO market_price_value 使用的媒体回传数据，要限制大小？
            logging.debug(f"proc_id={multiprocessing.current_process().name},"
                          f"media_app_id:{media_app_id}, position_id:{position_id}, level:{level},"
                          f"len(impression_price_list):{len(impression_price_list)} < 10, data is sparse "
                          f"enough to compute")
        else:
            # e-e
            # market_price 市场价格
            # chosen_count_map = {}  # 记录选择次数
            # imp_count_map = {}  # 记录曝光次数
            market_price, chosen_count_map, imp_count_map = self.bandit(market_price_value,
                                                                        impression_price_list,
                                                                        no_impression_price_list)

            logging.info(f"calculate default data proc_id={multiprocessing.current_process().name},"
                         f"media_app_id:{media_app_id}, position_id:{position_id},"
                         f"history_median_price_value:{market_price_value}, market_price:{market_price}，"
                         f"len impression_price_list:{len(impression_price_list)}, "
                         f"len no_impression_price_list:{len(no_impression_price_list)}")

            # 设置市场价格调整比例
            get_adjust_ratio(logging, media_app_id, position_id, -1, impression_price_list,
                             market_price, chosen_count_map, imp_count_map, ecpm_norm_dict, optimal_ratio_dict)

        return optimal_ratio_dict

    def calculate_delta(self, total_count, k_chosen_count):
        # total_count->目前的试验次数，k_chosen_count->是这个臂被试次数
        if k_chosen_count < 1:
            k_chosen_count = 1

        return math.sqrt(2 * math.log(total_count) / float(k_chosen_count))

    def calculate_reward_weigth(self, price, market_price_value, right_range, left_range):
        """
        计算reward权重
        """
        reward = 0.01
        if market_price_value * 0.9 < price <= market_price_value * 1.1:
            reward = 0.9
        elif price > market_price_value * 1.1:
            reward = 1 - ((price - market_price_value) / right_range)
            if reward > 0.9:
                reward = 0.9
        else:
            reward = 1 - ((market_price_value - price) / left_range)
            if reward > 0.9:
                reward = 0.9

        return reward

    def bandit_init(self, impression_price_list, no_impression_price_list, market_price_value):
        """
        # bandit 初始化
        """
        estimared_rewards_map = {}  # 记录reward
        chosen_count_map = {}  # 记录选择次数
        imp_count_map = {}  # 记录曝光次数

        right_range = max(abs(impression_price_list[-1] - market_price_value), 1)
        left_range = max(abs(market_price_value - impression_price_list[0]), 1)

        # 步骤1：初始化
        for price in impression_price_list:  # 曝光数据
            if price not in chosen_count_map:
                chosen_count_map[price] = 1
            else:
                chosen_count_map[price] += 1

            if price not in imp_count_map:  # 响应有曝光
                imp_count_map[price] = 1
            else:
                imp_count_map[price] += 1

        for price in no_impression_price_list:  # 响应未曝光
            # price_set.add(price)
            if price not in chosen_count_map:
                chosen_count_map[price] = 1
            else:
                chosen_count_map[price] += 1

        for price in chosen_count_map.keys():
            rate = 0.0
            if price in imp_count_map:
                rate = float(imp_count_map[price]) / chosen_count_map[price]

            estimared_rewards_map[price] = rate * self.calculate_reward_weigth(price,
                                                                               market_price_value,
                                                                               right_range,
                                                                               left_range)

        return chosen_count_map, imp_count_map, estimared_rewards_map

    def bandit(self, market_price_value, impression_price_list, no_impression_price_list):
        """
        e-e探索：UCB方式
        """
        Dis_Image = Distributed_Image(logging)
        # right_range = max(abs(impression_price_list[-1] - market_price_value), 1)
        # left_range = max(abs(market_price_value - impression_price_list[0]), 1)
        # 步骤1：初始化
        chosen_count_map, imp_count_map, estimared_rewards_map = self.bandit_init(impression_price_list,
                                                                                  no_impression_price_list,
                                                                                  market_price_value)

        true_chosen_count_map = copy.deepcopy(chosen_count_map)
        true_imp_count_map = copy.deepcopy(imp_count_map)

        # 步骤2：选top
        chosen_key_set = list(chosen_count_map.keys())
        if len(chosen_count_map) > max_search_num:
            # 为了减少计算时间只取top max_search_num 进行计算
            chosen_count_sorted = sorted(chosen_count_map.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            chosen_key_set = set((i[0] for i in chosen_count_sorted[:max_search_num]))

        price_list = list(chosen_key_set)
        price_list = sorted(price_list, reverse=False)
        len_price_list = len(price_list)

        # 步骤3： bandit 计算
        sampling_imp_count = {}
        total_count = sum(chosen_count_map.values())
        old_chosen_count_map = chosen_count_map
        sampling_chosen_count_map = {}
        cal_num = min(len(imp_count_map) * 10, 5000)
        for sampling_freq in range(1, cal_num):
            max_upper_bound_probs = 0.0
            max_probs_key = 0
            total_count += sum(sampling_imp_count.values())
            # 步骤3：1、select arms
            for k in chosen_key_set:
                # TODO 加入beta期望、方差
                sampling_count = old_chosen_count_map[k]
                if k in sampling_chosen_count_map:
                    sampling_count += sampling_chosen_count_map[k]

                upper_bound_probs = estimared_rewards_map[k] + self.calculate_delta(total_count, sampling_count)
                if max_upper_bound_probs < upper_bound_probs:
                    max_upper_bound_probs = upper_bound_probs
                    max_probs_key = k

            if max_probs_key == 0:
                continue

            chosen_count_map[max_probs_key] += 1
            if max_probs_key not in sampling_chosen_count_map:
                sampling_chosen_count_map[max_probs_key] = 0
            sampling_chosen_count_map[max_probs_key] += 1

            min_market_price = max_probs_key
            # 步骤3：2、update
            if max_probs_key in imp_count_map and max_probs_key in imp_count_map:
                # np.random.randn(1)[0] -> 改为基于历史数据的采样
                # beta 先验  float(imp_count_map[max_probs_key]) / chosen_count_map[max_probs_key]
                sample_rate = np.random.beta(imp_count_map[max_probs_key],
                                             chosen_count_map[max_probs_key] - imp_count_map[max_probs_key])
                is_win = np.random.binomial(1, sample_rate)
                index = price_list.index(max_probs_key)

                if is_win == 1:
                    # 选择的max_probs_key能曝光，向左搜索（减价）
                    index = price_list.index(max_probs_key)
                    index -= 1
                    while index >= 0:
                        tmp_price = price_list[index]
                        if tmp_price not in imp_count_map or imp_count_map[tmp_price] < 1 \
                                or chosen_count_map[tmp_price] - imp_count_map[tmp_price] < 1:
                            break

                        sample_rate = np.random.beta(imp_count_map[tmp_price],
                                                     chosen_count_map[tmp_price] - imp_count_map[tmp_price])
                        is_win = np.random.binomial(1, sample_rate)
                        if is_win == 1:
                            # 向小于方向探索
                            index -= 1
                        else:
                            break

                    index += 1
                else:
                    # 选择的max_probs_key不能曝光，向右搜索（加价）
                    index += 1
                    while index < len_price_list:
                        tmp_price = price_list[index]
                        if tmp_price not in imp_count_map or imp_count_map[tmp_price] < 1 \
                                or chosen_count_map[tmp_price] - imp_count_map[tmp_price] < 1:
                            break

                        sample_rate = np.random.beta(imp_count_map[tmp_price],
                                                     chosen_count_map[tmp_price] - imp_count_map[tmp_price])
                        is_win = np.random.binomial(1, sample_rate)
                        if is_win != 1:
                            # 向大于方向探索
                            index += 1
                        else:
                            break

                    index -= 1
                    
                min_market_price = price_list[index]
                for x in chosen_count_map.keys():
                    if x not in imp_count_map:
                        imp_count_map[x] = 0

                    chosen_count_map[x] += 1
                    if x >= min_market_price:
                        imp_count_map[x] += 1

                        if x not in sampling_imp_count:
                            sampling_imp_count[x] = 0
                        sampling_imp_count[x] += 1

            curl_right_range = max(abs(impression_price_list[-1] - min_market_price), 1)
            curl_left_range = max(abs(min_market_price - impression_price_list[0]), 1)

            for price in chosen_key_set:

                if price not in sampling_imp_count:
                    continue
                rate = float(imp_count_map[price]) / chosen_count_map[price]
                reward_weight = self.calculate_reward_weigth(price, min_market_price, curl_right_range, curl_left_range)

                key_sample_freq = sampling_imp_count[price]

                # TODO: np.random.normal(rate, 1) 需要优化
                estimared_rewards_map[price] = (key_sample_freq * estimared_rewards_map[price] +
                                                reward_weight * np.random.normal(rate, 1)) / (key_sample_freq + 1)

        # 取reward最大值
        market_price = 0
        market_price_score = 0.0
        for price, value in estimared_rewards_map.items():
            if value > market_price_score:
                market_price_score = value
                market_price = price

        Dis_Image.win_rate_image(market_price_value, imp_count_map, chosen_count_map, impression_price_list[0])

        return market_price, chosen_count_map, imp_count_map

    def do_process(self, media_app_id, media_position_dict_obj, market_price_dict_obj, impression_price_dict_obj,
                   no_impression_obj, ecpm_norm_dict):
        """
        根据读取的数据，计算bid shading系数，输出至redis
        :return:
        """
        optimal_ratio_dict = {}

        if media_app_id not in media_position_dict_obj:
            return optimal_ratio_dict

        position_set = media_position_dict_obj[media_app_id]

        logging.info(f"proc_id={multiprocessing.current_process().name}, "
                     f"media_app_id:{media_app_id}, position_set:{position_set}")

        for position_id in position_set:
            # self.market_price_dict = media_app_id:position_id:pltv - value
            market_price = {}
            if media_app_id in market_price_dict_obj \
                    and position_id in market_price_dict_obj[media_app_id]:
                market_price = market_price_dict_obj[media_app_id][position_id]

            # self.impression_price_dict = media_app_id:position_id:pltv - value_list
            impression_price = {}
            if media_app_id in impression_price_dict_obj \
                    and position_id in impression_price_dict_obj[media_app_id]:
                impression_price = impression_price_dict_obj[media_app_id][position_id]

            # self.impression_price_dict = media_app_id:position_id:pltv - value_list
            no_impression_price = {}
            if media_app_id in no_impression_obj \
                    and position_id in no_impression_obj[media_app_id]:
                no_impression_price = no_impression_obj[media_app_id][position_id]

            if len(market_price) < 1 or len(impression_price) < 1 or len(no_impression_price) < 1:
                # 数据不合格跳过
                logging.info(f"len(market_price):{len(market_price)} < 1 "
                             f"or len(impression_price):{len(impression_price)} < 1 "
                             f"or len(no_impression_price):{len(no_impression_price)} < 1")
                continue

            self.calculate_market_price(media_app_id, position_id, market_price, impression_price,
                                        no_impression_price, ecpm_norm_dict, optimal_ratio_dict)

        return optimal_ratio_dict
