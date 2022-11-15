# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:19
# @Author  : biglongyuan
# @Site    : 
# @File    : config.py
# @Software: PyCharm

Environment = "offline"
Multi_Process = False
No_pltv = True
DATA_PATH = './data/bid_shading_2022102100_2022102110.txt'
TEST_DATA_PATH = './data/bid_shading_2022102111_2022102116.txt'

# 测试时的提价比例
INCREASE_RATIO = 1.5

# PLTV 分级信息
# PLTV_LEVEL = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PLTV_LEVEL = [1, 2, 3, 4]

# 并行数量
parallel_num = 6

# 最大搜索数量
max_search_num = 200000

# 最大迭代次数
max_sampling_freq = 1e7

# 迭代次数与历史数据的比例
sample_ratio = 10

# 存在redis的步长
ratio_step = 10

# 每个media - postion - pltv下最小的数据条数
DATA_NUMS_LOWER_BOUND = 1000
