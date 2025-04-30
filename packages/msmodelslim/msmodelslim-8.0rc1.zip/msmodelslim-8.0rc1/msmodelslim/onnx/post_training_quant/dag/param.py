# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
import onnx.helper
from onnx import numpy_helper
import numpy as np

from msmodelslim import logger


class Tensor:
    def __init__(self, value, dtype, shape, name):
        self._value = value
        self._dtype = dtype
        self._shape = shape
        self._name = name

    def __str__(self):
        return f'Tensor({self.name}): \tname={self.name}\tdtype={self.dtype}\t' \
               f'shape={self.shape}'

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        return self._value

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        return self._shape

    @property
    def name(self):
        return self._name

    @property
    def initializer(self):
        logger.debug("Export param: %s", self.name)
        if isinstance(self.value, np.ndarray):
            return numpy_helper.from_array(self.value, self.name)
        vals = self.value if isinstance(self.value, list) else [self.value]
        return onnx.helper.make_tensor(
            name=self.name,
            data_type=self.dtype,
            dims=self.shape,
            vals=vals
        )

    @value.setter
    def value(self, value):
        self._value = value

    @dtype.setter
    def dtype(self, value):
        self._dtype = value

    @shape.setter
    def shape(self, value):
        self._shape = value

    @name.setter
    def name(self, value):
        self._name = value


class NodeParam:
    def __init__(self, tensor, idx):
        self.tensor = tensor
        self.idx = idx

    def __str__(self):
        return f'NodeParam({self.tensor.name}): \ttensor={self.tensor}\tidx={self.idx}\t'

    def __repr__(self):
        return self.__str__()
