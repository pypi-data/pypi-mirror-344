# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
import numpy as np
import onnx
import onnxruntime as ort
from onnxruntime.quantization import CalibrationDataReader

from msmodelslim.onnx.post_training_quant.util import check_and_get_calib_data


class DataReader(CalibrationDataReader):
    def __init__(self, model_path=None, calib_data=None, quant_cfg=None):
        model = onnx.load(model_path)
        self.data = self._get_and_check_data(model, calib_data, quant_cfg)
        self.data_size = len(self.data)
        self.enum_data = None

    def __iter__(self):
        return self

    def __next__(self):
        result = self.get_next()
        if result is None:
            raise StopIteration
        return result

    def get_next(self):
        if self.enum_data is None:
            self.enum_data = iter(self.data)
        return next(self.enum_data, None)

    def rewind(self):
        self.enum_data = None

    def _get_and_check_data(self, model, calib_data, quant_cfg=None):
        session = ort.InferenceSession(model.SerializeToString())
        model_inputs = session.get_inputs()
        return check_and_get_calib_data(model_inputs, calib_data, quant_cfg)
