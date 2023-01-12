# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 10:04
# @Author  : biglongyuan
# @Site    : 
# @File    : market_price_distributed.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import json
import pandas as pd


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

        # plt.show()

    def true_history_win_rate(self, imp_count_map, chosen_count_map):
        win_rate = {
            i: imp_count_map[i] / chosen_count_map[i] for i in imp_count_map.keys()
        }

        fig = plt.figure(dpi=300)
        plt.scatter(win_rate.keys(), win_rate.values(), s=10)

        # plt.show()

    def true_pred_win_rate(self, pred_imp_count_map, pred_chosen_count_map, true_imp_count_map, true_chosen_count_map,
                           market_price_value, min_imp_price, name, revenue_rate_list, sampling_chosen_count_map):
        pred_win_rate = {}
        for i in pred_chosen_count_map.keys():
            if i in pred_imp_count_map.keys() and i in pred_chosen_count_map.keys() and pred_chosen_count_map[i] > 0:
                pred_win_rate[i] = pred_imp_count_map[i] / pred_chosen_count_map[i]
            else:
                pred_win_rate[i] = 0

        true_win_rate = {}
        true_win_rate_acc = {}
        acc_imp = 0
        acc_chosen = 0

        for k in true_chosen_count_map.keys():
            if k in true_imp_count_map.keys():
                true_win_rate[k] = true_imp_count_map[k] / true_chosen_count_map[k]
                acc_imp += true_imp_count_map[k]
            else:
                true_win_rate[k] = 0
            acc_chosen += true_chosen_count_map[k]
            true_win_rate_acc[k] = acc_imp / acc_chosen

        for i in pred_win_rate.keys():
            if i >= market_price_value:
                _market_price_value = i
                break
        plt.figure(dpi=300)
        plt.title("{} distribution".format(name))
        plt.scatter(pred_win_rate.keys(), pred_win_rate.values(), c='r', s=5, label="pred")
        plt.scatter(true_win_rate.keys(), true_win_rate.values(), c='blue', s=5, alpha=0.5, label='true')
        plt.scatter(true_win_rate_acc.keys(), true_win_rate_acc.values(), c='black', s=5, alpha=0.5, label='true_acc')
        # plt.scatter(sampling_chosen_count_map.keys(),
        #             np.array(list(sampling_chosen_count_map.values())) / max(sampling_chosen_count_map.values()),
        #             c='green', s=5, alpha=0.5, label='sample_nums', marker='o')
        plt.scatter(_market_price_value, pred_win_rate[_market_price_value], c="green", marker="^")
        if min_imp_price in pred_win_rate:
            plt.scatter(min_imp_price, pred_win_rate[min_imp_price], c="green", marker="*")

        plt.legend()

        [media_app_id, position_id] = name.split('_')
        figure_dir = "./figure/{}".format(media_app_id)
        if not os.path.exists(figure_dir):
            os.makedirs(figure_dir)

        plt.savefig(figure_dir + "/pred_win_rate_media_{}_position_{}.png"
                    .format(media_app_id, position_id))
        # plt.show()

        # 绘制 reward ratio 变化曲线
        sample_index = 0
        sample_revenue_rate_list = {}
        while sample_index < min(10000, len(revenue_rate_list)):
            sample_revenue_rate_list[sample_index] = revenue_rate_list[sample_index]
            if sample_index < 1000:
                sample_index += 10
            else:
                sample_index += 100

        plt.figure(dpi=300)
        plt.title("{} reward ratio".format(name))
        plt.scatter(sample_revenue_rate_list.keys(), sample_revenue_rate_list.values(), s=5)

        plt.savefig(figure_dir + "/reward_ratio_media_{}_position_{}.png"
                    .format(media_app_id, position_id))
        # plt.show()

    def loop_win_rate(self, pred_imp_count_map, pred_chosen_count_map, true_imp_count_map, true_chosen_count_map, name):
        pred_win_rate = {}
        for i in pred_chosen_count_map.keys():
            if i in pred_imp_count_map.keys():
                pred_win_rate[i] = pred_imp_count_map[i] / pred_chosen_count_map[i]
            else:
                pred_win_rate[i] = 0

        true_win_rate = {}
        true_win_rate_acc = {}
        acc_imp = 0
        acc_chosen = 0

        for k in true_chosen_count_map.keys():
            if k in true_imp_count_map.keys():
                true_win_rate[k] = true_imp_count_map[k] / true_chosen_count_map[k]
                acc_imp += true_imp_count_map[k]
            else:
                true_win_rate[k] = 0
            acc_chosen += true_chosen_count_map[k]
            true_win_rate_acc[k] = acc_imp / acc_chosen

        color_list = ['g', 'r', 'y', 'b']

        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 12})
        fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=300)
        marker_list = ['*', 'v', 'o', 'p', '^']

        plt.title("{} distribution".format(name))
        ax.plot(list(map(float, pred_win_rate.keys())),
                pred_win_rate.values(), label="pred win rate",
                linestyle='-',
                marker=marker_list[0],
                markersize='6')
        ax.plot(list(map(float, true_win_rate.keys())),
                true_win_rate.values(),
                label="true win rate",
                linestyle='-',
                marker=marker_list[1],
                markersize='6')
        ax.plot(list(map(float, true_win_rate_acc.keys())),
                true_win_rate_acc.values(),
                label="true acc win rate",
                linestyle='-',
                marker=marker_list[2],
                markersize='6')
        plt.legend()

        # [media_app_id, position_id] = name.split('_')
        # figure_dir = "./figure/{}".format(media_app_id)
        # if not os.path.exists(figure_dir):
        #     os.makedirs(figure_dir)
        #
        # plt.savefig(figure_dir + "/pred_win_rate_media_{}_position_{}.png"
        #             .format(media_app_id, position_id))
        plt.show()

    def win_rate_std_plot(self, win_rate, name):
        color_list = ['g', 'r', 'y', 'b']
        i = 0

        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 12})
        fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=300)
        marker_list = ['*', 'v', 'o', 'p', '^']

        # 设置刻度
        ax.tick_params(axis='both')
        # 显示网格
        ax.grid(True, linestyle='-.')
        ax.yaxis.grid(True, linestyle='-.')

        plt.figure(dpi=300)
        ax.plot(list(map(float, win_rate.keys())),  win_rate.values, label="win rate std", linestyle='-', marker=marker_list[i],
                markersize='6')

        ax.set_xlabel("arm name")

        # fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
        # 添加图例
        legend = ax.legend(loc='center right')


        # [media_app_id, position_id] = name.split('_')
        # figure_dir = "./figure/{}".format(media_app_id)
        # if not os.path.exists(figure_dir):
        #     os.makedirs(figure_dir)
        #
        # plt.savefig(figure_dir + "/pred_win_rate_media_{}_position_{}.png"
        #             .format(media_app_id, position_id))
        plt.show()

def main():
    Dis = Distributed_Image(1)
    bandit_result_path_name = "exp_1/bandit_result_2023011019_bid_shading_xmly_2022102109_2022102120_exp_1.json"
    evaluation_result_path_name = "../result/evaluation_result_2022123016_exp_arm30.json"
    with open(f"../result/{bandit_result_path_name}", mode='r', encoding='utf-8') as f:
        bandit_result = json.load(f)

        for key, dict in bandit_result.items():
            # if key in ["30633_36893", "30633_36565"]:
            if True:
                record_nums = dict.keys()
                record_nums_list = []
                for num in record_nums:
                    try:
                        record_nums_list.append(int(num))
                    except:
                        continue

                true_imp_count_map = dict["true_imp_count_map"]
                true_chosen_count_map = dict["true_chosen_count_map"]
                print("select max loop nums", max(record_nums_list))
                last_loop_dict = dict[str(max(record_nums_list))]
                # 绘制最后一次迭代的预测竞得率曲线
                Dis.loop_win_rate(last_loop_dict["imp_count_map"], last_loop_dict["chosen_count_map"],
                                  true_imp_count_map, true_chosen_count_map, key)


                # # 对迭代过程中的各arm的竞得率进行展示，均值方差
                # record_dict = {}
                # for num in record_nums_list:
                #     arm_win_rate_dict = {}
                #     for arm_num in dict[str(num)]["chosen_count_map"].keys():
                #         try:
                #             arm_win_rate_dict[arm_num] = dict[str(num)]["imp_count_map"][arm_num] / dict[str(num)]["chosen_count_map"][arm_num]
                #         except:
                #             arm_win_rate_dict[arm_num] = 0
                #     record_dict[num] = arm_win_rate_dict
                # record_df = pd.DataFrame(record_dict).T
                # record_arm_std = np.std(record_df)
                # Dis.win_rate_std_plot(record_arm_std, key)


if __name__ == '__main__':
    main()