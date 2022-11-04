# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:19
# @Author  : biglongyuan
# @Site    : 
# @File    : config.py
# @Software: PyCharm

# 获取曝光数据
yky_dsp_redis_sample_conf = {
    "host": "ssd54.sample.imkd.db",
    "port": 50054,
    "auth": "rumBGHegdk224PmE",
    "timeout": 1000,
    "pool_size": 300,
    "keepalive_time": 120 * 1000
}

# 限制读最近曝光的时间
read_impression_last_hour = 48

# env
Environment = "offline"

# 获取position ID 曝光 win_price中位数
position_median_price_day_key = "strategy-media-pos-pltv-median"  # 天更新
position_median_price_hour_key = "strategy-market-price-media-pos-pltv-median"  # 小时

# 写到线上 redis key
redis_key = "yky:dsp:bidshading_ee:marketprice:pos"

# PLTV 分级信息
# PLTV_LEVEL = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PLTV_LEVEL = [1, 2, 3, 4]

# 并行数量
parallel_num = 14

# 最大搜索数量
max_search_num = 100

# 存在redis的步长
ratio_step = 10

# rainbow configs
rainbow_bid_shading_white_list_name = "strategyService.bidShading"
yky_dsp_rainbow_conf = {
    "connectStr": "api.rainbow.oa.com:8080",
    "tokenConfig": {
        "app_id": "4d8bf0dd-032a-4743-8815-21bc5d34cb1d",
        "user_id": "42edaaa716c54e4fbef95571d6bd720d",
        "secret_key": "de0db5b1c823e5e10a88796f7038d69ba65c"
    },
}