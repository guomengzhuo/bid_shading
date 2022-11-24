# -*- coding: utf-8 -*-
# @Time    : 2022/11/22 11:09
# @Author  : biglongyuan
# @Site    : 
# @File    : bernoulliArm.py
# @Software: PyCharm

import random


class BernoulliArm(object):
    def __init__(self, p):
        self.p = p

    def draw(self):
        # reward system based on Bernoulli
        if random.random() > self.p:
            return 0.0

        return 1.0
