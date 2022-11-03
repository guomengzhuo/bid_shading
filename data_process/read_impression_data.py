# -*- coding: utf-8 -*-
# @Time    : 2022/9/28 09:52
# @Author  : biglongyuan
# @Site    : 
# @File    : read_impression_data.py
# @Software: PyCharm

import datetime
import redis
import json
import os


class ReadImpressionPriceData(object):
    """
    # 获取实时曝光价格
    """

    def __init__(self, logging, redis_conf):
        self.logging = logging
        self.redis_conf = redis_conf

    def get_local_data(self, begin, redis_prefix_key):
        data_res = []
        read_part = 0
        data_dict = {}
        read_time_set = set()
        file_path = f"{os.getcwd()}/data"
        begin = int(begin)
        if not os.path.exists(file_path):
            return False, data_res, read_part, data_dict, read_time_set

        file_list = os.listdir(file_path)

        if len(file_list) < 1:
            return False, data_res, read_part, data_dict, read_time_set

        file_name_end = ""
        end_time = 0
        for file_name in file_list:
            self.logging.info(f"file_name:{file_name}")
            file_name_sp = file_name.split("-")
            if len(file_name_sp) != 2:
                continue

            if file_name_sp[0] == redis_prefix_key:
                time = int(file_name_sp[1].split(".")[0])
                if time > end_time:
                    end_time = time
                    if file_name_end != "":
                        del_file_name = f"{file_path}/{file_name_end}"
                        self.logging.info(f"del_file_name:{del_file_name}")
                        os.remove(del_file_name)  # 删除过期文件

                    file_name_end = file_name

                else:
                    del_file_name = f"{file_path}/{file_name}"
                    self.logging.info(f"del_file_name:{del_file_name}")
                    os.remove(del_file_name)  # 删除过期文件

        if file_name_end == "":
            return False, data_res, read_part, data_dict, read_time_set

        with open(f"{file_path}/{file_name_end}", 'r') as f:
            self.logging.info(f"open {file_path}/{file_name_end}")
            data_dict = json.loads(f.read())
            self.logging.info(f"len data_dict:{len(data_dict)}")

        for key, value in data_dict.items():
            if int(key) >= begin:
                read_time_set.add(int(key))
                read_part += 1
                data_res.extend(value)
                # self.logging.info(f"key:{key}, begin:{begin}, read_part:{read_part}")

        if read_part > 1:
            return True, data_res, read_part, data_dict, read_time_set

        return False, data_res, read_part, data_dict, read_time_set

    def write_data_to_local(self, data_dict, redis_prefix_key, time_part_end):
        if not os.path.exists(f"{os.getcwd()}/data"):
            os.makedirs(f"{os.getcwd()}/data")
            self.logging.info(f"makedirs {os.getcwd()}/data")

        file_name = f"{os.getcwd()}/data/{redis_prefix_key}-{time_part_end}.json"
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                json.dump(data_dict, f)
                self.logging.info(f"write json data complete ./data/{redis_prefix_key}-{time_part_end}.json")
        else:
            self.logging.info(f"{file_name} is exist")

    def get_data_from_redis(self, redis_prefix_key, statis_minus_begin, statis_minus_end, date_len=12):
        assert len(str(statis_minus_begin)) == date_len and len(str(statis_minus_end)) == date_len and \
               int(statis_minus_begin) <= int(statis_minus_end)
        redis_client = redis.Redis(host=self.redis_conf["host"],
                                   port=self.redis_conf["port"],
                                   password=self.redis_conf["auth"])

        statis_minus_begin = str(statis_minus_begin)
        statis_minus_end = str(statis_minus_end)

        begin = datetime.datetime(int(statis_minus_begin[:4]), int(statis_minus_begin[4:6]),
                                  int(statis_minus_begin[6:8]), int(statis_minus_begin[8:10]),
                                  int(statis_minus_begin[10:12]))

        end = datetime.datetime(int(statis_minus_end[:4]), int(statis_minus_end[4:6]),
                                int(statis_minus_end[6:8]), int(statis_minus_end[8:10]),
                                int(statis_minus_end[10:12]))

        request_part = int((end - begin).seconds / 60) + 1
        data_res = []
        read_part = 0
        data_dict = {}
        read_time_set = set()

        has_data, _data_res, _read_part, _data_dict, _time_set = self.get_local_data(begin.strftime("%Y%m%d%H%M"),
                                                                                     redis_prefix_key)
        if has_data:
            data_res = _data_res
            read_part = _read_part
            data_dict = _data_dict
            read_time_set = _time_set
            self.logging.info(f"redis_prefix_key:{redis_prefix_key}, len read_time_set:{len(read_time_set)}")

        time_part_end = ""
        with redis_client.pipeline(transaction=False) as pipe:
            time_part_list = []
            while begin <= end:
                time_part = begin.strftime("%Y%m%d%H%M")
                if int(time_part) in read_time_set:
                    # self.logging.info(f"time_part:{time_part} in read_time_set")
                    begin = begin + datetime.timedelta(minutes=1)
                    continue

                redis_key = '_'.join([redis_prefix_key, 'p', time_part])
                time_part_list.append(time_part)
                self.logging.info(f'[get {redis_key} from redis ...]')
                pipe.get(redis_key)
                begin = begin + datetime.timedelta(minutes=1)

            if len(time_part_list) > 0:
                pipeline_execute_results = pipe.execute()

                self.logging.info(f"len(pipeline_execute_results):{len(pipeline_execute_results)}")
                for i in range(len(pipeline_execute_results)):
                    if pipeline_execute_results[i] is None:
                        self.logging.error(f"pipeline_execute_results[{i}] is None")
                        continue

                    read_part += 1
                    res = json.loads(pipeline_execute_results[i])

                    res_new = []
                    for r in res:
                        if isinstance(r, str):
                            r = json.loads(r)

                        res_new.append(r)

                    data_res.extend(res_new)
                    time_part_end = time_part_list[i]
                    data_dict[time_part_end] = res_new
                # 将数据本地化存储
                self.write_data_to_local(data_dict, redis_prefix_key, time_part_end)
            else:
                self.logging.info(f"len(time_part_list) = 0")



        return request_part == read_part, read_part, data_res

    def read_from_redis(self, is_impression=True, last_hour=4):
        """
        read from redis, first priority
        """
        output_dict = {}
        redis_prefix_key = 'st_account_impr'
        price_label = "win_price"
        if not is_impression:
            # 获取响应未曝光数据
            redis_prefix_key = 'st_account_no_impr'
            price_label = "ecpm"

        now_time = datetime.datetime.now()

        statis_minus_end = now_time.strftime("%Y%m%d%H%M")
        statis_minus_begin = (now_time + datetime.timedelta(hours=-last_hour)).strftime("%Y%m%d%H%M")
        self.logging.info(f"redis_prefix_key:{redis_prefix_key}, "
                          f"statis_minus_begin:{statis_minus_begin}, statis_minus_end:{statis_minus_end}")

        is_succ, data_num, data_res = self.get_data_from_redis(redis_prefix_key, statis_minus_begin, statis_minus_end)
        self.logging.info(f"redis_prefix_key:{redis_prefix_key}, is_succ:{is_succ}, data_num:{data_num}")

        if len(data_res) < 1:
            self.logging.info("len(data_res) < 1")
            return output_dict

        for line in data_res:
            #  impression:{'bucket_id': 5, 'media_app_id': 30415, 'win_price': 449, 'adgroup_id': 32422005,
            #  'account_id': 10000113, 'ad_type': 10005, 'pv': 1, 'pltv': 1, 'app_id': 107746, 'creative_id': 40955004,
            #  'position_id': 35474, 'statis_date': '202209281515'}

            # no_impression:{"media_app_id":30545,"ecpm":359.115784,"pv":1,"pltv":5,"creative_id":41195012,"position_id":37104}
            if "media_app_id" not in line or "position_id" not in line or "pltv" not in line:
                self.logging.info(f"media_app_id or position_id or pltv not in line:{line}")
                continue

            media_app_id = int(line["media_app_id"])
            position_id = int(line["position_id"])
            pltv = int(line["pltv"])

            if price_label not in line or "pv" not in line:
                self.logging.info(f"{price_label} or pv not in line")
                continue

            if int(line["pv"]) == 0:
                self.logging.info("int(line[pv]) == 0")
                continue

            value = int(line[price_label]) / int(line["pv"])
            if media_app_id not in output_dict:
                output_dict[media_app_id] = {}

            position_dict = output_dict[media_app_id]
            if position_id not in position_dict:
                position_dict[position_id] = {}

            pltv_dict = position_dict[position_id]
            if pltv not in pltv_dict:
                pltv_dict[pltv] = []

            pltv_dict[pltv].append(int(value))
            position_dict[position_id] = pltv_dict
            output_dict[media_app_id] = position_dict

        # self.logging.info(f"output_dict:{output_dict}")
        return output_dict


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d ]in %(funcName)-8s  %(message)s"
    )
    from configs.config import yky_dsp_redis_sample_conf

    rd = ReadImpressionPriceData(logging, yky_dsp_redis_sample_conf)
    rd.read_from_redis(is_impression=True, last_hour=1)
