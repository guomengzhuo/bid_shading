# -*- coding: utf-8 -*-
# @Time    : 2022/9/28 10:38
# @Author  : biglongyuan
# @Site    : 
# @File    : test.py
# @Software: PyCharm


from multiprocessing import Pool
import multiprocessing
import time

d = {}


class BidShading(object):
    def __init__(self):
        self.d = {}
        self.g = {1: 2}
        self.c = {1: 2}

    def func(self, i, j, z):
        l = {}
        l[i] = i * j
        l = self.f(l)
        return {i: j}

    def func_1(self, i):
        print(f"proc_id={multiprocessing.current_process().name}")
        return {1: 2}

    def f(self, l):
        l[2] = 3
        return l

    def run(self):
        p = Pool(5)
        res_l = []
        j = 199
        a_dict = multiprocessing.Manager().dict(self.g)
        for i in range(10):
            # res = p.apply_async(self.func, args=(i+j, j, a_dict))
            res = p.apply_async(self.func_1, args=(i, ))
            res_l.append(res)
            # print(f"======{i}======")

        p.close()  # 关闭进程池，不再接受请求
        p.join()  # 等待所有的子进程结束

        for res in res_l:
            print(f"res:{res.get()}")
            d.update(res.get())

        print(d)


if __name__ == '__main__':
   b = BidShading()
   b.run()

