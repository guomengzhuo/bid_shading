# -*- coding: utf-8 -*-

# curl -X POST -d '{"inputs": {"mdate":[11],"media_app_id":[2001],"position_id":[30020],"ecpm":[11],
# "market_price":[100]}}' http://localhost:8501/v1/models/dlf:predict

import requests
import json


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
        pre_result[ecpm_min] = win_rate
        ecpm_min += gap

    return pre_result


if __name__ == '__main__':
    mdate = 11
    media_app_id = 30633
    ecpm_min = 0
    ecpm_max = 7000
    gap = 10
    market_price = 100

    final_result = {}

    for position_id in [36893, 36565]:
        final_result[f"{media_app_id}_{position_id}"] = predict(mdate, media_app_id, position_id, ecpm_min, ecpm_max, gap, market_price)

    with open(f"./evaluation_result_dnn.json", mode='w', encoding='utf-8') as f:
        json.dump(final_result, f)
