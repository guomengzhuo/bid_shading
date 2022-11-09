# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm
import json

import numpy as np
import pandas as pd
from configs.config import DATA_PATH, INCREASE_RATIO


class ReadData(object):
    """
    # 数据读取主类
    """

    def __init__(self, logging, data_path=DATA_PATH):
        """
        # 初始化
        """
        self.logging = logging
        self.data_path = data_path

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

    def data_discret_norm(self, data_pd):
        data_pd = data_pd.copy()

        data_pd["key"] = data_pd["media_app_id"].map(str)\
            .str.cat([data_pd["position_id"].map(str), data_pd["pltv"].map(str)], sep="_")
        # 归一化 + 离散化
        for key, group_pd in data_pd.groupby(["key"]):
            if len(group_pd) < 100:
                continue
            # self.logging.info(f"{key}: data nums: {len(group_pd)}")

            # 归一化
            # group_pd["norm_min"] = group_pd["response_ecpm"].min()
            group_pd["norm_min"] = 0
            group_pd["norm_max"] = group_pd["response_ecpm"].max()
            group_pd["norm_ecpm"] = (group_pd["response_ecpm"] - group_pd["norm_min"]) \
                                    / (group_pd["norm_max"] - group_pd["norm_min"])

            data_pd.loc[data_pd["key"] == key, "norm_min"] = group_pd["norm_min"]
            data_pd.loc[data_pd["key"] == key, "norm_max"] = group_pd["norm_max"]
            data_pd.loc[data_pd["key"] == key, "norm_ecpm"] = group_pd["norm_ecpm"]

            # 离散化
            bins = pd.qcut(group_pd["norm_ecpm"], q=100, retbins=True)[1]
            bins[0] = 0

            data_pd.loc[data_pd["key"] == key, "interval"] = pd.qcut(group_pd["norm_ecpm"], q=100)
            data_pd.loc[data_pd["key"] == key, "interval_index"] = pd.qcut(group_pd["norm_ecpm"], q=100, labels=False)
            data_pd.loc[data_pd["key"] == key, "bins"] = json.dumps(list(bins))

        data_pd = data_pd.dropna()
        # 将 win_price 和 winner_bid_price 也归一化
        data_pd["win_price"] = (data_pd["win_price"] - data_pd["norm_min"]) / (data_pd["norm_max"] - data_pd["norm_min"])
        data_pd["winner_bid_price"] = (data_pd["winner_bid_price"] - data_pd["norm_min"]) / (data_pd["norm_max"] - data_pd["norm_min"])
        # 直接用离散化的右边界替换原来的ecpm
        data_pd["response_ecpm"] = data_pd["interval"].map(lambda x: x.right)
        data_pd["interval_index"] = data_pd["interval_index"].map(int)
        return data_pd

    def get_data_dict_struct(self, data_pd, is_imp=True):
        response_dict = {}
        for index, row in data_pd.iterrows():
            # self.logging.info(f"index:{index}, row:{row}")
            media_app_id = int(row["media_app_id"])
            position_id = int(row["position_id"])
            pltv = int(row["pltv"])
            value = float(row["response_ecpm"])
            # value = float(row["interval_index"])
            # if is_imp:
            #     value = float(row["win_price"])

            if media_app_id not in response_dict:
                response_dict[media_app_id] = {}

            position_dict = response_dict[media_app_id]
            if position_id not in position_dict:
                position_dict[position_id] = {}

            pltv_dict = position_dict[position_id]
            if pltv not in pltv_dict:
                pltv_dict[pltv] = []

            pltv_dict[pltv].append(value)
            position_dict[position_id] = pltv_dict
            response_dict[media_app_id] = position_dict

        return response_dict

    def data_process(self):
        """
        main function
        """
        market_price_dict = {}
        response_dict = {}
        norm_dict = {}

        # 1、获取本地数据
        data_pd = self.read_csv_data()
        data_pd = self.data_filter(data_pd)
        data_pd = self.data_discret_norm(data_pd)

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

        # 4、获取其他需要回传的数据
        for key, group_pd in data_pd.groupby(["key"]):
            [media_app_id, position_id, pltv] = map(int, key.split("_"))
            write_line = group_pd.iloc[0]
            if media_app_id not in norm_dict:
                norm_dict[media_app_id] = {}
            if position_id not in norm_dict[media_app_id]:
                norm_dict[media_app_id][position_id] = {}

            norm_dict[media_app_id][position_id][pltv] = {
                "norm_min": write_line["norm_min"],
                "norm_max": write_line["norm_max"],
                "bins": write_line["bins"]
            }

        self.logging.info(f"len imp_dict:{len(imp_dict)},  len no_imp_dict:{len(no_imp_dict)}, "
                          f"len market_price_dict:{len(market_price_dict)}")
        return market_price_dict, imp_dict, no_imp_dict, norm_dict

    def test_data_process(self):
        """
        read test dataset
        """
        # 获取本地数据
        data_pd_test = self.read_csv_data()

        # todo(@mfishzhang) 测试集是否需要过滤95分位数
        data_pd_test = self.data_filter(data_pd_test)

        data_pd_test["key"] = data_pd_test["media_app_id"].map(str)\
            .str.cat([data_pd_test["position_id"].map(str), data_pd_test["pltv"].map(str)], sep="_")
        data_pd_test["target_price"] = data_pd_test[["win_price", "winner_bid_price"]].T.max()
        data_pd_test["virtual_ecpm"] = data_pd_test["response_ecpm"] * INCREASE_RATIO

        return data_pd_test[["key", "response_ecpm", "target_price", "virtual_ecpm"]]


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.data_process()
