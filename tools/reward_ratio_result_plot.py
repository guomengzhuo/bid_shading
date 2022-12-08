# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 10:04
# @Author  : biglongyuan
# @Site    : 
# @File    : market_price_distributed.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
import os
import json
import logging
import pandas as pd

class Reward_Ratio_Image(object):
    """
    # 画图
    """
    def __init__(self, logging):
        """
        # 初始化
        """
        self.logging = logging

    def reward_ratio_image(self, result_dict, name):
        result_pd = pd.DataFrame(result_dict).T
        result_pd["index"] = result_pd.index.astype(float) / 1000
        if result_pd.empty:
            return

        cpm_norm = max(max(result_pd["cpm_mab"]), max(result_pd["cpm_br"]))

        # 解决中文显示问题
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(1, 1, dpi=300)
        # fig = plt.figure(dpi=300)
        plt.title("{} distribution".format(name))
        ax_sub = ax.twinx()
        ax_sub.scatter(result_pd["index"], result_pd["win_rate_mab"], c='r', s=5, label="win rate mab")
        ax.plot(result_pd["index"], result_pd["cpm_mab"], c='b', label="cpm mab")
        ax.set_ylabel("avg cpm")
        ax_sub.set_ylabel("win rate")
        # ax_sub.set_ylim([0, 1])
        ax.set_xlabel("iterations (thousand)")

        axLine, axLabel = ax.get_legend_handles_labels()
        ax_subLine, ax_subLable = ax_sub.get_legend_handles_labels()
        fig.legend(axLine + ax_subLine, axLabel + ax_subLable, loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)

        # [media_app_id, position_id] = name.split('_')
        # figure_dir = "./figure/{}".format(media_app_id)
        # if not os.path.exists(figure_dir):
        #     os.makedirs(figure_dir)
        #
        # plt.savefig(figure_dir + "/reward_ratio_during_loops_media_{}_position_{}.png"
        #             .format(media_app_id, position_id))
        plt.show()

    def one_metrics_image(self, result_dict, name, metrics='win_rate'):
        result_pd = pd.DataFrame(result_dict).T
        result_pd["index"] = result_pd.index.astype(float) / 1000
        if result_pd.empty:
            return

        plot_cols = []
        color_list = ['b', 'r', 'black', 'g']
        for col_name in result_pd.columns:
            if metrics in col_name:
                plot_cols.append(col_name)

        cpm_norm = max(max(result_pd["cpm_mab"]), max(result_pd["cpm_br"]))

        fig, ax = plt.subplots(1, 1, dpi=300)
        # fig = plt.figure(dpi=300)
        plt.title("{} {} distribution".format(name, metrics))
        for i in range(len(plot_cols)):
            ax.scatter(result_pd["index"], result_pd[plot_cols[i]], c=color_list[i], s=5, label=plot_cols[i])
        ax.set_ylabel(metrics)
        ax.set_xlabel("iterations (thousand)")

        fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)

        # [media_app_id, position_id] = name.split('_')
        # figure_dir = "./figure/{}".format(media_app_id)
        # if not os.path.exists(figure_dir):
        #     os.makedirs(figure_dir)
        #
        # plt.savefig(figure_dir + "/reward_ratio_during_loops_media_{}_position_{}.png"
        #             .format(media_app_id, position_id))
        plt.show()


def main():
    with open("../result/evaluation_result_2022120717.json", mode='r',
              encoding='utf-8') as f:
        evaluation_dict = json.load(f)

        for key, dict in evaluation_dict.items():
            if key in ["30633_36893", "30633_36565"]:
                for metrics in ["rr", "win_rate", "cpm", "price_elasticity", "revenue", "surplus"]:
                    Reward_Ratio_Image.one_metrics_image(logging, dict, key, metrics)


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    main()