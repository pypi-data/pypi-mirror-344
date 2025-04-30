# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
from copy import deepcopy
import os
from os import path
import inspect

from onnxruntime.quantization import QuantFormat, QuantType, quantize_static, CalibrationMethod
import onnx

from ascend_utils.common.security import get_valid_write_path, SafeWriteUmask
from msmodelslim.onnx.post_training_quant.dag.parser import parse_model, get_depthwise_node
from msmodelslim.onnx.post_training_quant.label_free.data_reader import DataReader
from msmodelslim.onnx.post_training_quant.label_free.rollback_quant_nodes import match_activations, \
    get_rollback_nodes
from msmodelslim import logger
from msmodelslim.onnx.post_training_quant.util import get_quantized_nodes, ONNX_MODEL_SUFFIX, \
    LF_QUANTIZED_OP_TYPES


def quantize_model(input_model_path, output_model_path, quant_config):
    model_name, _ = path.splitext(path.split(output_model_path)[1])
    cpu_quant_model_path = path.join(path.dirname(output_model_path), model_name + "_cpu_quant.onnx")
    cpu_quant_model_path = get_valid_write_path(cpu_quant_model_path, extensions=ONNX_MODEL_SUFFIX)

    data_reader = DataReader(input_model_path,
                             quant_config.calib_data, quant_config)
    logger.info("%s batch data to calibrate.", data_reader.data_size)
    if quant_config.amp_num > 0:
        rollback_data_reader = deepcopy(data_reader)

    if quant_config.is_signed_quant:
        quant_type = QuantType.QInt8
    else:
        quant_type = QuantType.QUInt8

    quantized_nodes = get_quantized_nodes(input_model_path, quantize_nodes=quant_config.quantize_nodes,
                                          exclude_nodes=quant_config.exclude_nodes)
    depthwise_nodes = get_depthwise_node(input_model_path)
    if not quant_config.is_quant_depthwise_conv:  # exclude depthwise conv
        quantized_nodes = list(set(quantized_nodes) - set(depthwise_nodes))

    logger.info("%s node will be quantized: %s", len(quantized_nodes), quantized_nodes)

    quant_kwargs = {
        "quant_format": QuantFormat.QOperator,
        "per_channel": quant_config.is_per_channel,
        "op_types_to_quantize": LF_QUANTIZED_OP_TYPES,
        "activation_type": quant_type,
        "weight_type": quant_type,
        "nodes_to_quantize": quantized_nodes,
    }
    
    # onnxruntime版本升级至1.17.0后取缔"optimize_model"参数，但是在低版本时"optimize_model"有且默认为True
    if 'optimize_model' in inspect.signature(quantize_static).parameters:
        quant_kwargs["optimize_model"] = False

    # onnxruntime will generate a temp model file named augmented_model.onnx in the quantization process
    temp_model_file = os.path.join(os.getcwd(), "augmented_model.onnx")
    temp_model_file = get_valid_write_path(temp_model_file)
    with SafeWriteUmask():
        quantize_static(input_model_path, cpu_quant_model_path, data_reader, **quant_kwargs)

    if quant_config.amp_num > 0:
        activation_errors = match_activations(input_model_path, cpu_quant_model_path, quantized_nodes, quant_config)
        rollback_nodes = get_rollback_nodes(input_model_path, activation_errors, quant_config.amp_num)
        logger.info("%s nodes are rollback.", rollback_nodes)
        quantized_nodes = list(set(quantized_nodes).difference(set(rollback_nodes)))
        quant_kwargs.update({"nodes_to_quantize": quantized_nodes})
        with SafeWriteUmask():
            quantize_static(input_model_path, cpu_quant_model_path, rollback_data_reader, **quant_kwargs)

    if os.path.exists(temp_model_file):
        logger.debug("Remove temp model file: %s.", temp_model_file)
        os.remove(temp_model_file)

    logger.info("Finish to quantize model on cpu.")

    logger.info("Convert quantized model to npu affinity model")
    cpu_model = onnx.load(cpu_quant_model_path)
    cpu_graph = parse_model(cpu_model)
    cpu_graph.convert_graph_lf_quant()
    cpu_graph.reduce_redundant_quant_node()
    cpu_graph.save_model(output_model_path)

    logger.debug("Remove temp cpu quant model file: %s", cpu_quant_model_path)
    if os.path.exists(cpu_quant_model_path):
        os.remove(cpu_quant_model_path)
