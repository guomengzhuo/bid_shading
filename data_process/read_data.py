# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm


from configs.config import DATA_PATH
import pandas as pd
import numpy as np


class ReadData(object):
    """
    # 数据读取主类
    """

    def __init__(self, logging, env="prob"):
        """
        # 初始化
        """
        self.logging = logging
        self.env = env
        self.data_path = DATA_PATH

    def read_csv_data(self):

        df = pd.read_csv(self.data_path, sep="\t")
        # df['pltv'] = df['pltv'].apply(pd.to_numeric, errors='coerce').fillna(0)
        # df['pctcvr'] = df['pctcvr'].apply(pd.to_numeric, errors='coerce').fillna(0.0)
        data_pd = df.astype({
            'tdbank_imp_date': np.str
            , 'media_app_id': np.int64
            , 'position_id': np.int64
            , 'pltv': np.int64
            , 'pctcvr': np.float64
            , 'pctr': np.float
            , 'bid_price': np.float
            , 'response_ecpm': np.float
            , 'win_price': np.float
            , 'winner_bid_price': np.float
        })

        self.logging.info(f"data_pd:{data_pd.head(10)}")
        return data_pd

    def data_filter(self, data_pd):
        tmp = data_pd[data_pd['win_price'] > 0]  # win_price>0
        win_price_list = np.array(tmp['win_price'])
        per_95 = np.percentile(win_price_list, 95)  # 95 分位数
        self.logging.info(f"pre_95:{per_95}, median:{np.median(win_price_list)}")
        data_pd = data_pd[data_pd['win_price'] <= per_95]  # 过滤 95 分位数

        self.logging.info(f"data_pd:{data_pd.head(10)}")
        return data_pd

    def get_data_dict_struct(self, data_pd, is_imp=True):
        response_dict = {}
        for index, row in data_pd.iterrows():
            # self.logging.info(f"index:{index}, row:{row}")
            media_app_id = int(row["media_app_id"])
            position_id = int(row["position_id"])
            pltv = int(row["pltv"])
            value = int(row["response_ecpm"])
            if is_imp:
                value = int(row["win_price"])

            if media_app_id not in response_dict:
                response_dict[media_app_id] = {}

            position_dict = response_dict[media_app_id]
            if position_id not in position_dict:
                position_dict[position_id] = {}

            pltv_dict = position_dict[position_id]
            if pltv not in pltv_dict:
                pltv_dict[pltv] = []

            pltv_dict[pltv].append(int(value))
            position_dict[position_id] = pltv_dict
            response_dict[media_app_id] = position_dict

        return response_dict

    def data_process(self):
        """
        main function
        """
        market_price_dict = {}
        response_dict = {}

        # 1、获取本地数据
        data_pd = self.read_csv_data()
        data_pd = self.data_filter(data_pd)

        # 2、获取response_dict
        imp_dict = self.get_data_dict_struct(data_pd[data_pd['win_price'] > 0], True)
        no_imp_dict = self.get_data_dict_struct(data_pd[data_pd['win_price'] == 0], False)

        # 3、获取中位数
        for media_app_id, position_info in imp_dict.items():
            if media_app_id not in market_price_dict:
                market_price_dict[media_app_id] = {}

            position_dict = market_price_dict[media_app_id]
            for position_id, pltv_info in position_info.items():

                if position_id not in position_dict:
                    position_dict[position_id] = {}

                pltv_dict = position_dict[position_id]
                for pltv, win_price_list in pltv_info.items():
                    pltv_dict[pltv] = np.median(np.array(win_price_list))

                position_dict[position_id] = pltv_dict
            market_price_dict[media_app_id] = position_dict

        self.logging.info(f"len imp_dict:{len(imp_dict)},  len no_imp_dict:{len(no_imp_dict)}, "
                          f"len market_price_dict:{len(market_price_dict)}")
        return market_price_dict, imp_dict, no_imp_dict


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.data_process()
