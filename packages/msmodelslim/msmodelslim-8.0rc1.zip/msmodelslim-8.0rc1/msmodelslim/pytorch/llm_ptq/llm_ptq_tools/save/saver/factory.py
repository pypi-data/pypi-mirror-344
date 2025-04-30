# Copyright Huawei Technologies Co., Ltd. 2025. All rights reserved.
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.llm_ptq_utils import SAVE_TYPE_SAFE_TENSOR, SAVE_TYPE_NUMPY
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.saver.base import BaseSaver
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.saver.multi import MultiSaver
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.saver.npy import NpySaverConfig, NpySaver
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.saver.safetensors import SafetensorsSaverConfig, SafetensorsSaver


class SaverFactory:
    @staticmethod
    def create(typ, **kwargs) -> BaseSaver:
        if isinstance(typ, list):
            if len(typ) == 1:
                return SaverFactory.create(typ[0], **kwargs)
            return SaverFactory.create_multi_saver(typ, **kwargs)

        if not isinstance(typ, str):
            raise TypeError(f'Unsupported save type: {type(typ).__name__}')

        if typ == SAVE_TYPE_SAFE_TENSOR:
            return SaverFactory.create_safetensors_saver(typ, **kwargs)
        if typ == SAVE_TYPE_NUMPY:
            return SaverFactory.create_npy_saver(typ, **kwargs)
        raise ValueError(f'Unsupported save type: {type(typ).__name__}')

    @staticmethod
    def create_multi_saver(types, **kwargs) -> MultiSaver:
        saver = MultiSaver()
        for typ in types:
            saver.register(SaverFactory.create(typ, **kwargs))
        return saver

    @staticmethod
    def create_safetensors_saver(typ, **kwargs) -> SafetensorsSaver:
        output_dir = kwargs['output_dir']
        cfg = kwargs['cfg']
        safetensors_name = kwargs['safetensors_name']
        json_name = kwargs['json_name']
        part_file_size = kwargs['part_file_size']

        return SafetensorsSaverConfig(output_dir=output_dir,
                                      model_quant_type=cfg.model_quant_type,
                                      use_kvcache_quant=cfg.use_kvcache_quant,
                                      use_fa_quant=cfg.use_fa_quant,
                                      safetensors_name=safetensors_name,
                                      json_name=json_name,
                                      part_file_size=part_file_size).get_saver()

    @staticmethod
    def create_npy_saver(typ, **kwargs) -> NpySaver:
        output_dir = kwargs['output_dir']
        return NpySaverConfig(save_directory=output_dir).get_saver()
