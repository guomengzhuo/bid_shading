
'''
Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.

@File: redis_conf.py
@File Created: 2022-04-01 11:16:53
@Author: judezhang (judezhang@tencent.com)
@Brief: redis config
'''

# yky配置redis-深圳
yky_conf_redis_conf = {
    "production": {
        "host": "cache32.ykyconf.imkd.db",
        "port": 50032,
        "auth": "redisN5nP7bgU",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky配置redis-广州
yky_conf_redis_conf_gz = {
    "production": {
        "host": "cache3.ykyyxconf.yky.db",
        "port": 50003,
        "auth": "hUe8b1Zeg7HZEviT",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky-rtb redis 配置
yky_dsp_rtb_redis_conf = {
    "production": {
        "host": "cache6.ykyrtbconf.yky.db",
        "port": 50006,
        "auth": "kTpp16SWeK4KPbTg",
        "timeout": 1000,
        "pool_size": 30,
        "keepalive_time": 120*1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}


# yky用户交叉特征redis-深圳
yky_user_cross_feature_redis_conf = {
    "production": {
        "host": "cache56.ykyusercrossft.imkd.db",
        "port": 50056,
        "auth": "J9Uj8UanoJU5pVDe",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky用户交叉特征redis-广州
yky_user_cross_feature_redis_conf_gz = {
    "production": {
        "host": "cache13.ykyusercrossft.yky.db",
        "port": 50013,
        "auth": "zGwbRHoVWgKssY3p",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky计费、预算控制、竞价响应redis-深圳
yky_cost_statistics_redis_conf = {
    "production": {
        "host": "cache29.kleindsp.imkd.db",
        "port": 50029,
        "auth": "redissdzNmIX",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky计费、预算控制、竞价响应redis-广州
yky_cost_statistics_redis_conf_gz = {
    "production": {
        "host": "cache2.ykyyxfeec.yky.db",
        "port": 50002,
        "auth": "ix2STLODmGYYkpdt",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky计费参数补偿redis-深圳
yky_bidresponse_monitor_url_param_redis_conf = {
    "production": {
        "host": "ssd58.paramcache.imkd.db",
        "port": 50058,
        "auth": "ojE2Mz9URXRyJ7Ik",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky计费参数补偿redis-广州
yky_bidresponse_monitor_url_param_redis_conf_gz = {
    "production": {
        "host": "ssd9.ykyparamcache.yky.db",
        "port": 50009,
        "auth": "WBVwq3QLLL9ftlvF",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky媒体结算数据服务redis-深圳
yky_report_service_redis_conf = {
    "production": {
        "host": "cache33.ykyreport.imkd.db",
        "port": 50033,
        "auth": "redisXdM6bidK",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# yky算法统计数据redis-广州
# 存储targetROI广告组数据
yky_algo_statics_redis_conf = {
    "production": {
        "host": "cache16.algstaticsconf.yky.db",
        "port": 50016,
        "auth": "JpBX65AeL6jIyXLh",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

# 算法策略redis-清远
# 存储双出价实时cpa
algo_strategy_redis_conf = {
    "production": {
        "host": "ssd54.sample.imkd.db",
        "port": 50054,
        "auth": "rumBGHegdk224PmE",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "test": {
        "host": "strategy.o2.imkd.db",
        "port": 50004,
        "auth": "redis@imkd",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}