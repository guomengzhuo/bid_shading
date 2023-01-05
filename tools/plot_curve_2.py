# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 10:57
# @Author  : biglongyuan
# @Site    :
# @File    : plot_curve_2.py
# @Software: PyCharm
# encoding=utf-8
import matplotlib.pyplot as plt
import matplotlib
import argparse


def read_data(file_name: str=""):
    x = []
    y = []
    header = []
    with open(file_name, 'r') as fr:
        index = 0
        for line in fr.readlines():
            index += 1
            if index == 1:
                header = line.strip().split(',')[1:]
                y = [[] for _ in header]
                continue
            data = line.strip().split(',')
            x.append(int(data[0]))
            for i, elem in enumerate(data[1:]):
                y[i].append(float(elem))
    return x, y, header


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='./论文图/reward消除实验/new_default_win_rate_record')
    parser.add_argument('--x_name', type=str, default='train_step')
    parser.add_argument('--y_name', type=str, default='Q-value')
    parser.add_argument('--num_step', type=int, default=300)
    parser.add_argument('--img_name', type=str, default='win_score_exp')
    args = parser.parse_args()
    x, y_list, header = read_data(args.file)
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 12})
    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=100)
    marker_list = ['*', 'v', 'o', 'p', '^']
    marker_list = marker_list[:len(y_list)]
    for i, (y, marker) in enumerate(zip(y_list, marker_list)):
        ax.plot(x[:args.num_step:12], y[:args.num_step:12], label=header[i], linestyle='-', marker=marker, markersize='6')
    ax.set_xlabel(args.x_name)
    ax.set_ylabel(args.y_name)
    # 设置刻度
    ax.tick_params(axis='both')
    # 显示网格
    ax.grid(True, linestyle='-.')
    ax.yaxis.grid(True, linestyle='-.')
    # 添加图例
    legend = ax.legend(loc='center right')
    plt.show()
    fig.savefig(f'{args.img_name}.pdf', format='pdf', dpi=100)