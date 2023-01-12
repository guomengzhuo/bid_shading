# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 10:33
# @Author  : biglongyuan
# @Site    :
# @File    : request.py
# @Software: PyCharm


# curl -X POST -d '{"inputs": {"mdate":[11],"media_app_id":[2001],"position_id":[30020],"ecpm":[11],
# "market_price":[100]}}' http://localhost:8501/v1/models/dlf:predict

import requests


def predict(mdate, media_app_id, position_id, ecpm, market_price=0):

    data = "{\"inputs\": {" + f"\"mdate\": [{mdate}],\"media_app_id\": [{media_app_id}], " \
                              f"\"position_id\": [{position_id}], \"ecpm\": [{ecpm}], " \
                              f"\"market_price\": [{market_price}]" + "}}"

    # data = """{"inputs": {"mdate": [11],
    #                "media_app_id": [2001],
    #                "position_id": [30020],
    #                "ecpm": [11],
    #                "market_price": [100]}
    #     }"""

    url = "http://localhost:8501/v1/models/dlf:predict"
    r = requests.post(url, data=data)

    print(r.json())
    return r.json().get('outputs').get('final_dead_rate')[0]


if __name__ == '__main__':
    mdate = 11
    media_app_id = 2001
    position_id = 30020
    ecpm = 11
    market_price = 100
    final_dead_rate = predict(mdate, media_app_id, position_id, ecpm, market_price)
    print(f"final_dead_rate:{final_dead_rate}")
