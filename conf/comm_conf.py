"""
Author: yasindu
Date: 2021-04-13 21:06:53
LastEditTime: 2021-04-13 21:07:27
LastEditors: yasindu
Description: comm_conf
FilePath: /Klein-DSP/script/conf/comm_conf.py
symbol_custom_string_obkoro1: @Copyright : Copyright (C) 2021 THL A29 Limited, a Tencent company. All rights reserved.
"""
yky_dsp_creative_ecpm = "yky_dsp_creative_ecpm"
yky_dsp_creative_cvr = "yky_dsp_creative_cvr"
yky_dsp_cold_start_creative = "yky_dsp_cold_start_creative"
yky_dsp_strategy_cold_start_creative = "yky_dsp_strategy_cold_start_creative"
yky_dsp_history_pltv = "yky_dsp_history_pltv"
yky_dsp_media_bidFloor_participation_rate = "yky_dsp_media_bidFloor_participation_rate"
yky_dsp_position_bandit = "yky_dsp_position_bandit"
yky_dsp_creative_embedding_vector = "yky_dsp_creative_embedding_vector"
yky_ad_position_level = "yky_ad_position_level"
yky_dsp_recall_creative_vector = "yky_dsp_recall_creative_vector"
yky_dsp_recall_material_vector = "yky_dsp_recall_material_vector"
yky_dsp_dcaf_creative_vector = "yky_dsp_dcaf_creative_vector"
yky_dsp_recall_creative_md5_redis_key = "yky_dsp_recall_creative_md5"
cpc_redis_key = "yky:adgroup:optimize_towards_action:cpc:factor"
rtb_cpc_redis_key = "yky_adgroup_calibrated_bid_price"
creative_statis_daily_api_path = "/yky/get_creative_statis_daily"
creative_statis_minutely_api_path = "/yky/get_adgroup_statis_minutely"


bkdata_conf = {
    "data_query_url": "http://iegdata.apigw.o.oa.com/prod/v3/dataquery/query/",
    "data_deploy_url": "http://bk-data.apigw.o.oa.com/prod/v3/access/deploy_plan/",
    "data_clean_url": "http://bk-data.apigw.o.oa.com/prod/v3/databus/cleans/",
    "dataflow_url": "http://bk-data.apigw.o.oa.com/prod/v3/dataflow/flow/flows/",
    "data_ticket_url": "http://bk-data.apigw.o.oa.com/prod/v3/auth/tickets/",
    "bkdata_data_token": "WzPm5hLMue0jlm421KZXcRvawvCBnOCMmJwbytrgBaZuXQM3TlmH4JtrpqrmVAu0",
    "bk_app_code": "mms",
    "bk_app_secret": "mz1TNZpOd3YxL3hmJEHrMoFvf1zBHKMVzrMp4jpxIfIldmWFPN"
}

# yky tof alarm conf
yky_tof_conf = {
    "sys_id": "25211",
    "appkey": "06d8a9336dcd485da83e5dc9d1feae7d"
}

#

# yky dsp db conf
yky_dsp_db_conf = {
    "production": {
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "dsp_svr",
        "passwd": "dsp_svr@#$",
        "database": "yky_conf"
    },
    "preview": {
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "dsp_svr",
        "passwd": "dsp_svr@#$",
        "database": "yky_conf"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    },
    "dev": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    }
}

# yky new dsp db conf
yky_new_dsp_db_conf = {
    "production": {
        "host": "11.177.159.68",
        "port": 3306,
        "user": "o2root",
        "passwd": "Ieg_o2-mkt-api!@#",
        "database": "o2mkt"
    },
    "test": {
        "host": "11.177.157.192",
        "port": 3306,
        "user": "o2root",
        "passwd": "Ieg_o2-mkt-api-test!@#",
        "database": "o2mkt"
    },
    "dev": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "database": "yky_conf"
    }
}

# yky new dsp platform id conf
yky_platform_id_conf = {
    "production": {
        "med_platform_id":80
    },
    "test": {
        "med_platform_id":80
    },
}

# yky dsp stat data db conf
yky_dsp_data_conf = {
    "production": {
        "host": "11.177.154.28",
        "port": 3306,
        "user": "yky_dsp",
        "passwd": "yky_dsp123",
        "database": "yky_dsp_data"
    },
    "preview": {
        "host": "11.177.154.28",
        "port": 3306,
        "user": "yky_dsp",
        "passwd": "yky_dsp123",
        "database": "yky_dsp_data"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    },
    "dev": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    }
}

# o2 db conf
o2_db_conf = {
    "production": {
        "host": "gamedb.gamedb.imkd.db",
        "port": 10000,
        "user": "ocpa-admin",
        "passwd": "ocpa-admin@#~",
        "database": "o2_conf"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#",
        "database": "yky_conf"
    },
    "dev": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    }
}

# monitor db
yky_dsp_monitor_db_conf = {
    "production": {
        "host": "spider.o2ocpx.imkd.db",
        "port": 25000,
        "user": "yky-dsp",
        "passwd": "yky-dsp@#$~123",
        "database": "yky_dsp_monitor"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "root",
        "passwd": "iegqwe!@#",
        "database": "yky_dsp_monitor"
    },
    "dev": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_dsp_monitor"
    }
}

# yky redis conf
yky_dsp_redis_conf = {
    "production": {
        "host": "cache32.ykyconf.imkd.db",
        "port": 50032,
        "auth": "redisN5nP7bgU",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "production_algo": {
        "host": "cache16.algstaticsconf.yky.db",
        "port": 50016,
        "auth": "JpBX65AeL6jIyXLh",
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    },
    "preview": {
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
    },
    "dev": {
        "host": "9.134.105.30",
        "auth": "redis@yky123",
        # "host": "9.134.107.57",
        # "auth": "yKCRU*3786pk",
        "port": 6380,
        "timeout": 1000,
        "pool_size": 300,
        "keepalive_time": 120 * 1000
    }
}

yky_dcaf_item_model = {
    "dev": {
        "model_name": "request_value_item_2.0",
        "host": "11.157.48.26",
        "port": "8501",
    },
    "test": {
        "model_name": "request_value_item_2.0",
        "host": "11.146.81.67",
        "port": "8501"
    },
    "production": {
        "model_name": "request_value_item_2.0",
        "host": "30.47.143.96",
        "port": "8501"
    }
}


yky_recall_item_model = {
    "dev": {
        "model_name": "item_recall",
        "host": "9.134.191.20",
        "port": "8501",
        # "host": "9.134.10.89",
        # "port": "7901"
    },
    "test": {
        "model_name": "item_recall",
        "host": "11.146.81.49",
        "port": "8501"
    },
    "production": {
        "model_name": "item_recall",
        "host": "30.47.141.80",
        "port": "8501"
    }
}

yky_lite_ranking_item_model = {
    "dev": {
        "model_name": "item_literanking",
        "host": "9.134.191.20",
        "port": "8501",
        # "host": "9.134.10.89",
        # "port": "7901"
    },
    "test": {
        "model_name": "item_literanking",
        "host": "11.146.81.65",
        "port": "8501"
    },
    "production": {
        "model_name": "item_literanking",
        "host": "30.47.141.90",
        "port": "8501"
    }
}

yky_recall_elastic_faiss = {
    "apis": {
        "put_api": "SearchEngine/put",
        "delete_api": "SearchEngine/del",
        "add_alias_api": "SearchEngine/add_alias",
        "get_alias_api": "SearchEngine/get_alias",
        "create_index_api": "SearchEngine/create_index",
        "rebuild_index_api": "SearchEngine/rebuild_index",
        "delete_index_api": "SearchEngine/delete_index",
        "info_index_api": "SearchEngine/get_index_state",
        "search_api": "SearchEngine/search",

    },
    "production": {
        "l5_addr": "normal.elasticfaiss.ef_yky_dsp_worker.main_port",
        "index_alias": "yky_dsp_model_recall",
    },
    "test": {
        "l5_addr": "64674945:65536",
        "index_alias": "yky_dsp_model_recall_test",
    },
    "dev": {
        "l5_addr": "64674945:65536",
        "index_alias": "yky_dsp_model_recall_dev",
    },
}

yky_dsp_tdbank = {
    "production": {
        "bid": "b_ieg_o2_rt",
        "item_model_feature_tid": "yky_dsp_recall_item_model_feature",
        "cold_start_creative_tid": "yky_recall_cold_start_creative_daily",
    },
    "test": {
        "bid": "b_ieg_o2_rt",
        "item_model_feature_tid": "yky_dsp_recall_item_model_feature",
        "cold_start_creative_tid": "yky_recall_cold_start_creative_daily",
    },
    "dev": {
        "bid": "b_ieg_o2_rt",
        "item_model_feature_tid": "yky_dsp_recall_item_model_feature_test",
        "cold_start_creative_tid": "yky_recall_cold_start_creative_daily",
    },
}

yky_dsp_rainbow_conf = {
    "connectStr": "api.rainbow.oa.com:8080",
    "tokenConfig": {
        "app_id": "4d8bf0dd-032a-4743-8815-21bc5d34cb1d",
        "user_id": "42edaaa716c54e4fbef95571d6bd720d",
        "secret_key": "de0db5b1c823e5e10a88796f7038d69ba65c"
    },
}
