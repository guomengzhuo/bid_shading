# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:19
# @Author  : biglongyuan
# @Site    : 
# @File    : config.py
# @Software: PyCharm

Environment = "offline"
DATA_PATH = "./data/bid_shading.csv"


# PLTV 分级信息
# PLTV_LEVEL = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PLTV_LEVEL = [1, 2, 3, 4]

# 并行数量
parallel_num = 6

# 最大搜索数量
max_search_num = 200000

# 存在redis的步长
ratio_step = 10

