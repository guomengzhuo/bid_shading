# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:19
# @Author  : biglongyuan
# @Site    : 
# @File    : config.py
# @Software: PyCharm

Environment = "offline"
Multi_Process = False
No_pltv = True
search_test = False
# DATA_PATH = './data/bid_shading_QB_2022102118_2022102120.txt'
# TEST_DATA_PATH = './data/bid_shading_QB_2022102121_2022102121.txt'
DATA_PATH = './data/bid_shading_xmly_2022102009_2022102020.txt'
TEST_DATA_PATH = './data/bid_shading_xmly_2022102109_2022102120.txt'

# 选择最优化的方式
OPTIMAL_COST = True

# 测试时的提价比例
INCREASE_RATIO = 1.5

# PLTV 分级信息
# PLTV_LEVEL = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PLTV_LEVEL = [1, 2, 3, 4]

# 离散化的分桶数量
BIN_NUMS = 100

# 并行数量
parallel_num = 6

# 最大搜索数量
max_search_num = 200000

# 最大迭代次数
max_sampling_freq = 100000

# 迭代次数与历史数据的比例
sample_ratio = 3

# 存在redis的步长
ratio_step = 10

# 每个media - postion - pltv下最小的数据条数
DATA_NUMS_LOWER_BOUND = 1000
