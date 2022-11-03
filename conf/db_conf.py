'''
Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.

@File: comm_conf.py
@File Created: 2021-03-15 21:16:53
@Author: neopi (neopi@tencent.com)
@Last Modified: 2021-03-15 21:16:53
@Modified By: neopi (neopi@tencent.com)
@Brief: some common conf, db conf, bkdata conf etc.
'''


# yky data db conf
yky_db_conf = {
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_data"
    },
    "production": {
        "host": "11.177.154.28",
        "port": 3306,
        "user": "sspdata",
        "passwd": "ssp@#$data",
        "database": "yky_data"
    }
}

dspadmin_db_conf = {
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "o2_conf"
    },
    "production": {
        "host": "11.177.154.22",
        "port": 3306,
        "user": "dspdata",
        "passwd": "dspdata!@#",
        "database": "yky_conf"
    },
}

sspadmin_db_conf = {
    "test": {
        "host": "gamedb.imkd-beta.imkd.db",
        "port": 10000,
        "user": "sspdata",
        "passwd": "WFrVfA87XrO4",
        "database": "ieg_ssp"
    },
    "production": {
        "host": "11.177.154.34",
        "port": 3306,
        "user": "sspdata",
        "passwd": "sspdata!@#",
        "database": "ieg_ssp"
    },
}


mms_db_conf = {
    "production": {
        "host": "mms.db.ied.com",
        "port": 3306,
        "user": "mmsadmindata",
        "passwd": "mmsadmin@#$data",
        "database": "mms_task"
    },
    "production-new": {
        "host": "gamedb.mms.imkd.db",
        "port": 10000,
        "user": "mmsadmindata",
        "passwd": "mmsadmin@#$data",
        "database": "mms_task"
    }
}

o2_db_conf = {
    "production": {
        "host": "gamedb.gamedb.imkd.db",
        "port": 10000,
        "user": "yky_data",
        "passwd": "yky@#$data",
        "database": "o2_conf"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "o2_conf"
    },
}

# ssp admin mango db conf
sspadmin_mongodb_conf = {
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
    },
    "dev": {
        "host": "11.185.155.149",
        "port": 27017,
        "user": "sspadmin",
        "passwd": "JhjP*TOHYvkz",
        "database": "ssp",
        "authentication_database": "admin"
    }
}


# yky conf db
yky_conf_db = {
    "production": {
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
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "root123456",
        "database": "yky_conf"
    }
}

# yky sys backend db conf
yky_sys_backend_db_conf = {
    "production": {
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "yky_sys_backend",
        "passwd": "yky_sys_backend@#$",
        "database": "errorno"
    },
    "preview": {
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "yky_sys_backend",
        "passwd": "yky_sys_backend@#$",
        "database": "errorno"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "yky_conf"
    },
    "dev": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "",
        "passwd": "",
        "database": "errorno"
    }
}

# yky_dsp_data
yky_dsp_data_db = {
    "production": {
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
        "database": "yky_dsp_data"
    },
    "dev": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "root123456",
        "database": "yky_dsp_data"
    }
}

yky_dsp_conf_db = {
    "production": {
        "host": "ykydsp.db.ied.com",
        "port": 3306,
        "user": "dsp_svr",
        "passwd": "dsp_svr@#$",
        "database": "yky_conf"
    }
}

ieg_ssp_conf_db = {
    "production": {
        "host": "11.177.154.34",
        "port": 3306,
        "user": "sspdata",
        "passwd": "sspdata!@#",
        "database": "ieg_ssp"
    }
}

yky_mc_data_db = {
    "production": {
        "host": "11.185.157.206",
        "port": 3306,
        "user": "mcdata",
        "passwd": "mcdata@#$data",
        "database": "yky_mc_data"
    },
    "dev": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "database": "yky_mc_data"
    }
}

yky_mc_conf_db = {
    "production": {
        "host": "11.185.157.206",
        "port": 3306,
        "user": "mcdata",
        "passwd": "mcdata@#$data",
        "database": "yky_mc_conf"
    },
    "dev": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "database": "yky_mc_conf"
    }
}

yky_mc_config_db = {
    "production": {
        "host": "11.181.32.61",
        "port": 3306,
        "user": "cultivation",
        "passwd": "cultivation@#$service",
        "database": "game_center"
    }
}

mc_report_db_conf = {
    "production": {
        'host': '11.185.157.206',
        'port': 3306,
        "user": "mc_data",
        "passwd": "Ieg_media-data!@#",
        'database': 'yky_mc_conf',
        'charset': 'utf8',
    },
}

yky_featureservice_db_conf = {
    "production": {
        "host": "11.148.212.153",
        "port": 3306,
        "user": "feature",
        "passwd": "IEG_feature!@#",
        "database": "feature_service"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "feature_service"
    },
    "dev": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "o2db",
        "passwd": "o2db",
        "database": "feature_service"
    }
}

yky_partner_db_conf = {
    "production": {
        "host": "11.181.32.61",
        "port": 3306,
        "user": "featuresvc",
        "passwd": "featuresvc@#$cultivation",
        "database": "game_center"
    },
    "test": {
        "host": "100.97.140.8",
        "port": 3307,
        "user": "cultivation",
        "passwd": "cultivation@#$service",
        "database": "game_center"
    },
}
