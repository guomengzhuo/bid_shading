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
        plt.title("{} reward ratio distribution".format(name))
        ax_sub = ax.twinx()
        # ax.scatter(result_pd["index"], result_pd["cpm_mab"]/cpm_norm, c='b', s=5, label="cpm (mab)")
        # ax.scatter(result_pd["index"], result_pd["cpm_br"]/cpm_norm, c='green', s=5, label="cpm (best ratio)")
        ax.scatter(result_pd["index"], result_pd["surplus_mab"], c='b', s=5, label="surplus (mab)")
        ax.scatter(result_pd["index"], result_pd["surplus_br"], c='green', s=5, label="surplus (best ratio)")
        ax.scatter(result_pd["index"], result_pd["surplus_upper_bound"], c='yellow', s=5, label="surplus upper bound")
        ax_sub.plot(result_pd["index"], result_pd["win_rate_mab"], c='r', label="win rate mab")
        ax_sub.plot(result_pd["index"], result_pd["win_rate_br"], c='black', label="win rate br (best ratio)")
        ax.set_ylabel("surplus")
        ax_sub.set_ylabel("win rate")
        ax_sub.set_ylim([0, 1])
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


def main():
    with open("../result/evaluation_result_2022120119.json", mode='r',
              encoding='utf-8') as f:
        evaluation_dict = json.load(f)

        for key, dict in evaluation_dict.items():
            Reward_Ratio_Image.reward_ratio_image(logging, dict, key)


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    main()