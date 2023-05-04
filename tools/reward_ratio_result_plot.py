# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
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
        # plt.show()

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
        # plt.show()

    def multiple_method_comparison(self, multi_method_result_dict, name, metrics='win_rate'):
        color_list = ['g', 'r', 'y', 'b']
        i = 0

        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 12})
        fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=300)
        marker_list = ['*', 'v', 'o', 'p', '^', 'h', 'd', 'X', '>']

        # 设置刻度
        ax.tick_params(axis='both')
        # 显示网格
        ax.grid(True, linestyle='-.')
        ax.yaxis.grid(True, linestyle='-.')

        for method, result_dict in multi_method_result_dict.items():
            result_pd = pd.DataFrame(result_dict).T
            result_pd["index"] = result_pd.index.astype(float) / 1000
            if result_pd.empty:
                return

            ax.plot(result_pd["index"], result_pd[metrics], label=method, linestyle='-', marker=marker_list[i],
                    markersize='6')
            # ax.scatter(result_pd["index"], result_pd[metrics], c=color_list[i], s=5, label=method)
            i += 1

        ax.set_ylabel(metrics)
        ax.set_xlabel("iterations (thousand)")

        # fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
        # 添加图例
        legend = ax.legend(loc='center right')

        [media_app_id, position_id] = name.split('_')
        # figure_dir = "./figure/{}".format(media_app_id)
        # if not os.path.exists(figure_dir):
        #     os.makedirs(figure_dir)

        # plt.savefig(figure_dir + "/method_analyse_media_{}_position_{}_{}.png"
        #             .format(media_app_id, position_id, metrics))
        plt.show()


def main():
    multimethod_evaluation_result_dict = {}
    multimethod_evaluation_name_dict = {
        "exp_arm30": "evaluation_result_2022121517_exp_arm30.json",
        # "arm_independent": "evaluation_result_2022121611_arm_independent.json",
        "exp_arm100": "evaluation_result_2022123016_1_exp_arm100.json"
    }
    for key, name in multimethod_evaluation_name_dict.items():
        with open(f"../result/{name}", mode='r',
                  encoding='utf-8') as f:
            singlemethod_evaluation_dict = json.load(f)
            for media_position, dict in singlemethod_evaluation_dict.items():
                if media_position not in multimethod_evaluation_result_dict.keys():
                    multimethod_evaluation_result_dict[media_position] = {}

                multimethod_evaluation_result_dict[media_position][key] = dict

    for key, dict in multimethod_evaluation_result_dict.items():
        if key in ["30633_36893", "30633_36565"]:
            # for metrics in ["surplus_mab"]:
            for metrics in ["win_rate_mab", "cpm_mab", "surplus_mab"]:
                Reward_Ratio_Image.multiple_method_comparison(logging, dict, key, metrics)


def mean_plot_main(method_list):
    result_path = './result'
    files = os.listdir(result_path)
    all_files, all_dirs = [], []

    for root, dirs, files in os.walk('./result'):
        for file in files:
            all_files.append(os.path.join(root, file))

        for dir in dirs:
            all_dirs.append(os.path.join(root, dir))

    multimethod_evaluation_name_dict = {}
    for method in method_list:
        multimethod_evaluation_name_dict[method] = method + ".json"

    multimethod_evaluation_result_dict = {}

    for key, name in multimethod_evaluation_name_dict.items():
        tmp_data_list = {}
        cnt = 0
        for file in all_files:
            if "evaluation_result" in file and name in file:
                with open(file, mode='r', encoding='utf-8') as f:
                    singlemethod_evaluation_dict = json.load(f)
                    cnt += 1
                    for media_position, dict in singlemethod_evaluation_dict.items():
                        if media_position not in tmp_data_list.keys():
                            tmp_data_list[media_position] = pd.DataFrame(dict)
                        else:
                            tmp_data_list[media_position] += pd.DataFrame(dict)

        for media_position, dict in tmp_data_list.items():
            if media_position not in multimethod_evaluation_result_dict.keys():
                multimethod_evaluation_result_dict[media_position] = {}
            multimethod_evaluation_result_dict[media_position][key] = (dict / cnt).dropna(axis=1).to_dict()

    for key, dict in multimethod_evaluation_result_dict.items():
        if key in ["30633_36893", "30633_36565"]:
        # if True:
            # for metrics in ["surplus_mab"]:
            for metrics in ["win_rate_mab", "cpm_mab", "surplus_mab"]:
                Reward_Ratio_Image.multiple_method_comparison(logging, dict, key, metrics)


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    mean_plot_main()