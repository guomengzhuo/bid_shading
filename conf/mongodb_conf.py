'''
Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.

@File: mysql_conf.py
@File Created: 2022-05-23 21:16:53
@Author: kintonhuang (kintonhuang@tencent.com)
@Last Modified: 2022-05-23 21:16:53
@Modified By: kintonhuang (kintonhuang@tencent.com)
@Brief: some mysql conf.
'''

# ssp管理端DB
ssp_admin_mongodb_conf = {
    "production": {
        "host": "11.185.157.196:27017,11.185.157.217:27017,11.185.157.182",
        "port": 27017,
        "user": "datacenter",
        "passwd": "p8#q88LrW4kT",
        "database": "ssp",
        "authentication_database": "admin"
    },
    "test": {
        "host": "11.185.155.149",
        "port": 27017,
        "user": "sspadmin",
        "passwd": "JhjP*TOHYvkz",
        "database": "ssp",
        "authentication_database": "admin"
    }
}
