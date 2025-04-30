# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
class Flip:
    def __init__(self, data, round_data, round_err, t_max=None, t_min=None, is_flip_up=True):
        self.is_flip_up = is_flip_up
        self.data = None
        self.error = None
        self.priority = None
        self.order = None
        self._init_flip_data(data, round_data, round_err, t_max, t_min)

    def reshape(self, shape):
        self.data = self.data.reshape(shape)
        self.error = self.error.reshape(shape)
        self.priority = self.error.reshape(shape)

    def _init_flip_data(self, data, round_data, round_err, t_max, t_min):
        if self.is_flip_up:
            # up_是考虑四舍五入时，小于0.5的值，原本是x->0.0，现在要考虑反向x->1.0
            self.data = round_data.copy()
            self.error = round_err.copy()
            self.error[data >= t_max] = 0.0
            self.error[self.error > 0] = 0.0
            self.priority = abs(self.error.copy())

            self.error[self.error != 0] += 1  # 向上近似的误差，即原来0.4四舍五入是0.4->0，现在0.4->1.0
            self.data[self.data != 0] += 1  # 将原本要近似到0.0的值，反向近似到1.0
        else:
            # down_是考虑四舍五入时，大于0.5的值，原本是x->1.0，现在要考虑反向x->0.0
            self.data = round_data.copy()
            self.error = round_err.copy()
            self.error[data <= t_min] = 0.0
            self.error[self.error < 0] = 0.0
            self.priority = abs(self.error.copy())

            self.error[self.error != 0] -= 1  # 向下近似的误差，即原来0.7四舍五入是0.7->1.0，现在0.7->0.0
            self.data[self.error != 0] -= 1  # 将原本要近似到1.0的值，反向近似到0.0
