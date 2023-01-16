# -*- coding: utf-8 -*-
# @Time    : 2023/1/16 10:21
# @Author  : biglongyuan
# @Site    : 
# @File    : calculateDelta.py
# @Software: PyCharm

import math


class CalculateDelta(object):
    def __init__(self):
        """
        初始化
        """

    def sqrt(self, total_count, k_chosen_count):
        # total_count->目前的试验次数，k_chosen_count->是这个臂被试次数
        if total_count == 0:
            return 0

        if k_chosen_count < 1:
            k_chosen_count = 1

        return math.sqrt(2 * math.log(total_count) / float(k_chosen_count))

    def moss(self, total_rounds, total_count, k_chosen_count):
        """
        total_rounds : the number of rounds
        k_chosen_count: switch times between arms
        """
        # total_count->目前的试验次数，k_chosen_count->是这个臂被试次数
        if total_count == 0:
            return 0

        if k_chosen_count < 1:
            k_chosen_count = 1

        return math.sqrt(max(math.log(total_rounds / k_chosen_count), 0) / float(total_count))

    def ucb_2(self, total_count, k_chosen_count):
        # total_count->目前的试验次数，k_chosen_count->是这个臂被试次数
        if total_count == 0:
            return 0

        if k_chosen_count > 50:
            k_chosen_count = 50

        tau = int(math.ceil((1 + self.alpha_param) ** k_chosen_count))

        if math.log(math.e * float(total_count) / tau) <= 0:
            return 0
        return math.sqrt((1. + k_chosen_count) * math.log(math.e * float(total_count) / tau) / (2. * tau))