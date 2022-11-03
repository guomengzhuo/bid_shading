'''
Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.

@File: mysql_conf.py
@File Created: 2022-05-23 21:16:53
@Author: kintonhuang (kintonhuang@tencent.com)
@Last Modified: 2022-05-23 21:16:53
@Modified By: kintonhuang (kintonhuang@tencent.com)
@Brief: some mysql conf.
'''

# DSP老管理端DB
yky_dsp_admin_db_conf = {
    "production": {
        # 11.177.154.22
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "dsp_svr",
        "passwd": "dsp_svr@#$"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#"
    }
}

# DSP新管理端DB
yky_dsp_admin_db_conf_new = {
    "production": {
        "host": "11.177.159.68",
        "port": 3306,
        "user": "o2root",
        "passwd": "Ieg_o2-mkt-api!@#"
    },
    "test": {
        "host": "11.177.157.192",
        "port": 3306,
        "user": "o2root",
        "passwd": "Ieg_o2-mkt-api-test!@#"
    }
}

# yky数据相关DB
# 存储由TDW出库的数据、注册回流等效果数据、创意漏斗数据、脚本监测告警的job和task数据等
yky_dsp_data_db_conf = {
    "production": {
        "host": "11.177.154.28",
        "port": 3306,
        "user": "yky_dsp",
        "passwd": "yky_dsp123"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#"
    }
}

# o2相关DB
# 存储O2游戏相关数据，如游戏id、游戏名称、游戏受众、游戏品类、安卓包名、apple应用包名等
o2_db_conf = {
    "production": {
        # 11.185.151.73
        "host": "gamedb.gamedb.imkd.db",
        "port": 10000,
        "user": "yky_data",
        "passwd": "yky@#$data"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#"
    }
}

# yky计费补偿数据DB
yky_feecalc_compensate_db_conf = {
    "production": {
        # 11.185.153.11
        "host": "spider.o2ocpx.imkd.db",
        "port": 25000,
        "user": "yky-dsp",
        "passwd": "yky-dsp@#$~123"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#"
    }
}

# 微信小游戏相关DB
# 存储源渠道、源平台名称、落地页拉起小游戏方式等数据
wx_game_db_conf = {
    "production": {
        # 111.230.187.250
        "host": "gz-cdb-7rmq1kef.sql.tencentcdb.com",
        "port": 57296,
        "user": "yky",
        "passwd": "1pl9omCpOXsq"
    },
    "test": {
        "host": "gz-cdb-7rmq1kef.sql.tencentcdb.com",
        "port": 57296,
        "user": "yky",
        "passwd": "1pl9omCpOXsq"
    }
}

# 特征工程组DB
yky_dsp_db_feature_conf = {
    "production": {
        "host": "11.185.148.205",
        "port": 3306,
        "user": "monitor",
        "passwd": "monitor!@#",
        "database": "yky_strategy"
    },
    "test": {
        "host": "11.185.148.205",
        "port": 3306,
        "user": "monitor",
        "passwd": "monitor!@#",
        "database": "yky_strategy"
    },
    "dev": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "xmqq123",
        "database": "yky_data_tdw"
    }
}