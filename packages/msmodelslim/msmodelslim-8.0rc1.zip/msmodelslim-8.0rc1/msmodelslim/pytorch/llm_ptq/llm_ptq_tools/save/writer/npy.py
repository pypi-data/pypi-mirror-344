# Copyright Huawei Technologies Co., Ltd. 2025. All rights reserved.
import os.path

import numpy as np
import torch

from ascend_utils.common.security import check_type, get_valid_write_path, SafeWriteUmask
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.writer.base import BaseWriter


class NpyWriter(BaseWriter):
    def __init__(self, logger, save_directory: str = '.', file_name: str = 'model.npy'):
        super().__init__(logger)

        self.save_directory = save_directory
        self.file_name = file_name
        self.dict = {}

    def save_param(self):
        output_path = os.path.join(self.save_directory, self.file_name)
        output_path = get_valid_write_path(output_path)
        with SafeWriteUmask(umask=0o377):
            np.save(output_path, self.dict)
        self.logger.info(f'Save npy to {output_path} successfully')

    def _write(self, key: str, value: torch.Tensor) -> None:
        check_type(value, torch.Tensor)
        self.dict[key] = value

    def _close(self) -> None:
        if not self.dict:
            return

        self.save_param()
        del self.dict
