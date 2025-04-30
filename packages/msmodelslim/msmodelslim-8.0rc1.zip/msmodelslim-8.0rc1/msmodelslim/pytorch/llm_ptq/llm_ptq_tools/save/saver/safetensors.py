# Copyright Huawei Technologies Co., Ltd. 2025. All rights reserved.
import os.path
from dataclasses import dataclass, field
from logging import Logger
from typing import Optional, Union

from msmodelslim import logger as msmodelslim_logger
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.llm_ptq_utils import SAVE_TYPE_SAFE_TENSOR
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.saver.base import BaseSaver
from msmodelslim.pytorch.llm_ptq.llm_ptq_tools.save.writer import BufferedSafetensorsWriter, JsonDescriptionWriter, \
    SafetensorsWriter


@dataclass
class SafetensorsSaverConfig:
    logger: Logger = field(init=False, default=msmodelslim_logger)

    output_dir: str
    model_quant_type: str
    use_kvcache_quant: bool = False
    use_fa_quant: bool = False

    safetensors_name: Optional[str] = 'quant_model_weight.safetensors'
    json_name: Optional[str] = 'quant_model_description.json'
    part_file_size: Optional[int] = None

    def __post_init__(self):
        if not isinstance(self.safetensors_name, str):
            default_safetensors_name = f"quant_model_weight_{self.model_quant_type.lower()}.safetensors"
            self.logger.warning(f"invalid `safetensors_name`, defaulting to `{default_safetensors_name}`")
            self.safetensors_name = default_safetensors_name
        if not isinstance(self.json_name, str):
            default_json_name = f"quant_model_description_{self.model_quant_type.lower()}.json"
            self.logger.warning(f"invalid `json_name`, defaulting to `{default_json_name}`")
            self.json_name = default_json_name

    @staticmethod
    def from_dict(d: dict):
        if isinstance(d, SafetensorsSaverConfig):
            return d
        if not isinstance(d, dict):
            raise TypeError(f'Safetensors save config must be an instance of dict, but got {type(d).__name__}')
        return SafetensorsSaverConfig(**d)

    def get_saver(self):
        return SafetensorsSaver(self)


class SafetensorsSaver(BaseSaver):
    type_ = SAVE_TYPE_SAFE_TENSOR

    def __init__(self, cfg: Union[SafetensorsSaverConfig, dict]):
        super().__init__()

        cfg = SafetensorsSaverConfig.from_dict(cfg)
        self.logger = cfg.logger

        if cfg.part_file_size is None:
            file_path = os.path.join(cfg.output_dir, cfg.safetensors_name)
            self.weight_writer = SafetensorsWriter(logger=self.logger, file_path=file_path)
        else:
            file_name_prefix = cfg.safetensors_name.replace('.safetensors', '')
            self.weight_writer = BufferedSafetensorsWriter(logger=self.logger,
                                                           max_gb_size=cfg.part_file_size,
                                                           save_directory=cfg.output_dir,
                                                           save_prefix=file_name_prefix)
        self.meta_writer = JsonDescriptionWriter(logger=self.logger,
                                                 model_quant_type=cfg.model_quant_type,
                                                 json_name=cfg.json_name,
                                                 save_directory=cfg.output_dir,
                                                 use_kvcache_quant=cfg.use_kvcache_quant,
                                                 use_fa_quant=cfg.use_fa_quant)

    def pre_process(self) -> None:
        pass

    def save(self, name, meta, data) -> None:
        self.weight_writer.write(name, data)
        self.meta_writer.write(name, meta)

    def post_process(self) -> None:
        self.weight_writer.close()
        self.meta_writer.close()

        self.logger.info(f'Safetensors weight saved successfully')
