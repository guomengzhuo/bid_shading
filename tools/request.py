# -*- coding: utf-8 -*-
# @Time    : 2022/12/22 10:33
# @Author  : biglongyuan
# @Site    :
# @File    : request.py
# @Software: PyCharm


# curl -X POST -d '{"inputs": {"mdate":[11],"media_app_id":[2001],"position_id":[30020],"ecpm":[11],
# "market_price":[100]}}' http://localhost:8501/v1/models/dlf:predict

import requests


def predict(mdate, media_app_id, position_id, ecpm_min, ecpm_max, gap, market_price=0):

    pre_result = {}
    url = "http://localhost:8501/v1/models/dlf:predict"
    while ecpm_min <= ecpm_max:
        data = "{\"inputs\": {" + f"\"mdate\": [{mdate}],\"media_app_id\": [{media_app_id}], " \
                                  f"\"position_id\": [{position_id}], \"ecpm\": [{ecpm_min}], " \
                                  f"\"market_price\": [{market_price}]" + "}}"

        # data = """{"inputs": {"mdate": [11],
        #                "media_app_id": [2001],
        #                "position_id": [30020],
        #                "ecpm": [11],
        #                "market_price": [100]}
        #     }"""
        r = requests.post(url, data=data)
        win_rate = r.json().get('outputs').get('final_dead_rate')[0]
        pre_result[str(ecpm_min)] = str(win_rate)
        ecpm_min += gap

    return {f"{media_app_id}_{position_id}": pre_result}


if __name__ == '__main__':
    mdate = 11
    media_app_id = 2001
    position_id = 30020
    ecpm_min = 0
    ecpm_max = 200
    gap = 10
    market_price = 100
    final_dead_rate = predict(mdate, media_app_id, position_id, ecpm_min, ecpm_max, gap, market_price)
    print(f"final_dead_rate:{final_dead_rate}")
