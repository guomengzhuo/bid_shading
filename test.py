# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 17:02
# @Author  : biglongyuan
# @Site    :
# @File    : read_data.py
# @Software: PyCharm


from data_process.read_impression_data import ReadImpressionPriceData
from configs.config import DATA_PATH
from pandas.core.frame import DataFrame
import pandas as pd


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

    def test_read(self):

        df = pd.read_csv(self.data_path, sep="\t")
        
        print(df)

    def read_csv_data(self):
        data_num = 0
        data_list = []
        with open(self.data_path, "r") as fr:
            for line in fr.readlines():
                data_num += 1
                if data_num == 1:
                    continue

                line = line.strip().split("\t")
                if len(line) != 11 or (int(line[-1]) == 0 and int(line[-2]) == 0):
                    continue

                data_list.append(line)

        self.logging.info(f"data_num:{data_num}, len(data_list):{len(data_list)}")


        return data_list

    def run(self):
        """
        main function
        """
        market_price_dict = self.read_market_price_data()
        impression_price_dict, no_impression_price_dict = self.read_impression_price_data()

        self.logging.info(f"len market_price_dict:{len(market_price_dict)},"
                          f"len impression_price_dict:{len(impression_price_dict)},"
                          f"len no_impression_price_dict:{len(impression_price_dict)}")

        return market_price_dict, impression_price_dict, no_impression_price_dict


if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )

    rd = ReadData(logging)
    rd.test_read()
