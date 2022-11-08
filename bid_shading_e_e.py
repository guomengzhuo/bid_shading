# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:01
# @Author  : biglongyuan
# @Site    :
# @File    : bid_shading_e_e.py
# @Software: PyCharm


import os
import sys

from multiprocessing import Pool
import multiprocessing

import datetime
from data_process.read_data import ReadData
from configs.config import PLTV_LEVEL, parallel_num, max_search_num, ratio_step, Environment
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import logging

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


class Bandit(object):
    """
    bid shading 主类
    """

    def __init__(self):
        """
        初始化
        """
        # self.logging = logging

    def calculate_market_price(self, media_app_id, position_id, market_price_dict,
                               impression_price_dict, no_impression_price, optimal_ratio_dict):
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
            self.get_adjust_ratio(media_app_id, position_id, level, impression_price_list,
                                  market_price, chosen_count_map, imp_count_map, optimal_ratio_dict)

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
            self.get_adjust_ratio(media_app_id, position_id, -1, impression_price_list,
                                  market_price, chosen_count_map, imp_count_map, optimal_ratio_dict)

        return optimal_ratio_dict

    def get_adjust_ratio(self, media_app_id, position_id, level, impression_price_list,
                         market_price, chosen_count_map, imp_count_map, optimal_ratio_dict):
        """
        设置市场价格调整比例
        """
        upper_bound = int(1.5 * market_price)
        if len(impression_price_list) > 1:
            upper_bound = int(max(impression_price_list[-1] * 1.1, 1.5 * market_price))

        lower_bound = int(market_price * 0.9)
        step = ratio_step

        if level == -1:
            key = f"{media_app_id}_{position_id}"
        else:
            key = f"{media_app_id}_{position_id}_{level}"

        if key not in optimal_ratio_dict:
            optimal_ratio_dict[key] = {}

        ecpm_list = np.arange(lower_bound, upper_bound, step)
        adjust_ratio = []
        for price in ecpm_list:
            if price <= market_price:
                adjust_ratio.append(1.0)
            else:
                assert upper_bound - market_price > 0

                y = self.search_optimal_price(price, chosen_count_map, imp_count_map)

                if y == 0:
                    y = ((price - market_price) * (market_price * 1.5 - market_price) /
                         (upper_bound - market_price) + market_price) / price

                y = max(y, (0.9 * market_price) / price)   # 设置调价下限
                adjust_ratio.append(y)

        optimal_ratio_dict[key]['adjust_ratio_list'] = adjust_ratio
        optimal_ratio_dict[key]['upper_bound'] = upper_bound
        optimal_ratio_dict[key]['lower_bound'] = lower_bound
        optimal_ratio_dict[key]['step'] = step

    def search_optimal_price(self, ecpm, chosen_count_map, imp_count_map):
        ratio = 0
        gain = 0

        for price, chosen_count in chosen_count_map.items():
            imp_count = 0
            if chosen_count < 1:
                continue

            if ecpm in imp_count_map:
                imp_count = imp_count_map[ecpm]

            # 最大化 impression rate * (ecpm - price)
            expect_gain = (imp_count * 1.0 / chosen_count) * (ecpm - price)
            if expect_gain > gain:
                gain = expect_gain
                ratio = price * 1.0 / ecpm

        return ratio

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

    def bandit(self, market_price_value, impression_price_list, no_impression_price_list):
        """
        e-e探索：UCB方式
        """
        estimared_rewards_map = defaultdict(int)  # 记录reward
        chosen_count_map = {}  # 记录选择次数
        imp_count_map = defaultdict(int)  # 记录曝光次数

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

        # 步骤2：选top
        chosen_key_set = list(chosen_count_map.keys())
        if len(chosen_count_map) > max_search_num:
            # 为了减少计算时间只取top max_search_num 进行计算
            chosen_count_sorted = sorted(chosen_count_map.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            chosen_key_set = set((i[0] for i in chosen_count_sorted[:max_search_num]))

        # 步骤3： bandit 计算
        cal_num = min(len(imp_count_map) * 10, 5000)
        for sampling_freq in range(1, cal_num):
            max_upper_bound_probs = 0.0
            max_probs_key = 0
            total_count = sum(chosen_count_map.values())
            # 步骤3：1、select arms
            for k in chosen_key_set:
                upper_bound_probs = estimared_rewards_map[k] + self.calculate_delta(total_count, chosen_count_map[k])
                if max_upper_bound_probs < upper_bound_probs:
                    max_upper_bound_probs = upper_bound_probs
                    max_probs_key = k

            if max_probs_key == 0:
                continue

            chosen_count_map[max_probs_key] += 1

            # 步骤3：2、update
            rate = 0.01
            if max_probs_key in imp_count_map and max_probs_key in imp_count_map:
                # rate = float(imp_count_map[max_probs_key]) / chosen_count_map[max_probs_key]
                # np.random.randn(1)[0] -> 改为基于历史数据的采样
                # beta 先验  float(imp_count_map[max_probs_key]) / chosen_count_map[max_probs_key]
                sample_rate = np.random.beta(imp_count_map[max_probs_key], chosen_count_map[max_probs_key] - imp_count_map[max_probs_key])
                is_win = np.random.binomial(1, sample_rate)
                if is_win == 1:
                    # 出价真实曝光率 或者 靠近market price 认为会曝光
                    imp_count_map[max_probs_key] += 1
                    for x in chosen_count_map.keys():
                        if x > max_probs_key:
                            imp_count_map[x] += 1
                            chosen_count_map[x] += 1
                            # 同时更新x的reward
                            reward_weight = self.calculate_reward_weigth(x, market_price_value, right_range,
                                                                         left_range)
                            estimared_rewards_map[x] = (chosen_count_map[x] * estimared_rewards_map[x] +
                                                        reward_weight * np.random.normal(rate, 1)) / (
                                                                               chosen_count_map[x] + 1)
                else:
                    for x in chosen_count_map.keys():
                        if x < max_probs_key:
                            chosen_count_map[x] += 1
                            # 同时更新x的reward
                            reward_weight = self.calculate_reward_weigth(x, market_price_value, right_range,
                                                                         left_range)
                            estimared_rewards_map[x] = (chosen_count_map[x] * estimared_rewards_map[x] +
                                                        reward_weight * np.random.normal(rate, 1)) / (
                                                                               chosen_count_map[x] + 1)

                rate = float(imp_count_map[max_probs_key]) / chosen_count_map[max_probs_key]
                if rate < 0.01:
                    rate = 0.01

            reward_weight = self.calculate_reward_weigth(max_probs_key, market_price_value, right_range, left_range)

            key_sample_freq = chosen_count_map[max_probs_key]

            # TODO: np.random.normal(rate, 1) 需要优化
            estimared_rewards_map[max_probs_key] = (key_sample_freq * estimared_rewards_map[max_probs_key] +
                                                    reward_weight * np.random.normal(rate, 1)) / (key_sample_freq + 1)

        # 取reward最大值
        market_price = 0
        market_price_score = 0.0
        for price, value in estimared_rewards_map.items():
            if value > market_price_score:
                market_price_score = value
                market_price = price

        # 计算竞得率
        """
        win_rate = {
            i: imp_count_map[i] / chosen_count_map[i] for i in chosen_count_map.keys()
        }

        for i in win_rate.keys():
            if i > market_price_value:
                _market_price_value = i
                break
        fig = plt.figure(dpi=300)
        plt.scatter(win_rate.keys(), win_rate.values(), s=10)
        plt.scatter(_market_price_value, win_rate[_market_price_value], c="r")

        plt.show()
        """
        return market_price, chosen_count_map, imp_count_map

    def do_process(self, media_app_id, media_position_dict_obj, market_price_dict_obj, impression_price_dict_obj,
                   no_impression_obj):
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
                                        no_impression_price, optimal_ratio_dict)

        return optimal_ratio_dict


class BidShading(object):
    """
    bid shading 主类
    """

    def __init__(self, logging):
        """
        初始化
        """
        self.logging = logging

        # 价格数据初始化
        self.market_price_dict = {}
        self.impression_price_dict = {}
        self.media_position_dict = {}
        self.no_impression_price_dict = {}

        self.PLTV_LEVEL = PLTV_LEVEL

        self.optimal_ratio_dict = {}

    def read_data(self):
        # 1、读取 bid shading输入数据
        rd = ReadData(logging=self.logging)

        # market_price_dict = media_app_id:position_id:pltv - value
        # impression_price_dict = media_app_id:position_id:pltv - value_list
        self.market_price_dict, self.impression_price_dict, \
            self.no_impression_price_dict = rd.data_process()

        self.logging.info(f"len market_price_dict:{len(self.market_price_dict)}, "
                          f"len impression_price_dict:{len(self.impression_price_dict)}")

        # 2、获取media、position映射关系
        for media_id, position_info in self.market_price_dict.items():

            if media_id not in self.media_position_dict:
                self.media_position_dict[media_id] = set(position_info.keys())
            else:
                self.media_position_dict[media_id] = self.media_position_dict[media_id] | set(position_info.keys())

        for media_id, position_info in self.impression_price_dict.items():

            if media_id not in self.media_position_dict:
                self.media_position_dict[media_id] = set(position_info.keys())
            else:
                self.media_position_dict[media_id] = self.media_position_dict[media_id] | set(position_info.keys())

        self.logging.info(f"media_position_dict:{self.media_position_dict}")

    def remove_local_backend(self):
        """
        删除临时文件
        :return:
        """
        return

    def run(self):
        self.logging.info("run -> start")

        pool = Pool(parallel_num)  # 构建进程池
        res_l = []  # 保存进程返回结果
        bandit = Bandit()

        # 1、读取相关要处理的的数据
        self.read_data()

        # 2、计算并保存数据
        mgr = multiprocessing.Manager()
        media_position_dict_obj = mgr.dict(self.media_position_dict)
        market_price_dict_obj = mgr.dict(self.market_price_dict)
        impression_price_dict_obj = mgr.dict(self.impression_price_dict)
        no_impression_obj = mgr.dict(self.no_impression_price_dict)

        for media_app_id in self.media_position_dict.keys():
            res = pool.apply_async(bandit.do_process,
                                   args=(media_app_id, media_position_dict_obj, market_price_dict_obj,
                                         impression_price_dict_obj, no_impression_obj))
            res_l.append(res)

        pool.close()  # 关闭进程池，不再接受请求
        pool.join()  # 等待所有的子进程结束

        for res in res_l:
            self.logging.info(f"res:{res}")
            self.optimal_ratio_dict.update(res.get())

        self.logging.info(f"run -> end len(optimal_ratio_dict):{len(self.optimal_ratio_dict)}")
        self.logging.info(f"output optimal_ratio_dict:{self.optimal_ratio_dict}")

        # 3、计算完 删除临时文件
        self.remove_local_backend()


def main():
    bs = BidShading(logging)
    bs.run()


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    main()
    