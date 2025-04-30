# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.
from copy import deepcopy

import onnx
import onnxruntime
import numpy as np

from msmodelslim import logger
from msmodelslim.onnx.post_training_quant.dag.node import QuantizableOnnxNode
from msmodelslim.onnx.post_training_quant.dag.parser import parse_model
from msmodelslim.onnx.post_training_quant.data_free.quantizer import ActivationQuantizer
from msmodelslim.onnx.post_training_quant.data_free.quantizer import WeightQuantizer
from msmodelslim.onnx.post_training_quant.util import get_quantized_nodes, check_and_get_calib_data


def quantize_model(input_model_path, output_model_path, quant_config):
    quantized_nodes = get_quantized_nodes(input_model_path, quantize_nodes=quant_config.quantize_nodes,
                                          exclude_nodes=quant_config.exclude_nodes)
    logger.info("%s node will be quantized: %s", len(quantized_nodes), quantized_nodes)

    ori_model = onnx.load(input_model_path)
    onnx_graph = parse_model(ori_model, quantized_nodes)

    build_activations(deepcopy(ori_model), onnx_graph, quantized_nodes, quant_config)

    for node_name, node in onnx_graph.node_map.items():
        if not isinstance(node, QuantizableOnnxNode):
            continue
        logger.info("Quantized node: %s", node.name)
        activation_quantizer = ActivationQuantizer(name=node_name, is_signed=quant_config.is_signed_quant)
        activation_quantizer(node.activation)
        node.activation_scale = activation_quantizer.scale
        node.activation_offset = activation_quantizer.offset

        w_quantizer = WeightQuantizer(name=node.params[0], is_per_channel=quant_config.is_per_channel)
        w_quantizer(node.params[0].tensor.value)
        node.weight_offset = w_quantizer.offset
        node.weight_scale = w_quantizer.scale
        node.quant_weight = w_quantizer.quant_weight.astype(np.int8)

    onnx_graph.convert_graph_df_quant()
    onnx_graph.save_model(output_model_path)


def build_activations(model, onnx_graph, quantized_nodes, quant_config=None):
    for name in quantized_nodes:
        # 将卷积算子的父节点的输出加到模型的输出中，以获得卷积算子的输入，即activation
        onnx_node = onnx_graph.node_map.get(name)
        for input_x in onnx_node.inputs:
            model.graph.output.extend([onnx.ValueInfoProto(name=input_x)])

    ort_session = onnxruntime.InferenceSession(model.SerializeToString())
    inputs = ort_session.get_inputs()
    if quant_config and quant_config.calib_data:
        calib_data = check_and_get_calib_data(inputs, quant_config.calib_data)
    else:
        calib_data = check_and_get_calib_data(inputs)
    output = ort_session.run([], calib_data[0])
    activations = output[len(onnx_graph.outputs):]
    for i, act in enumerate(activations):
        name = quantized_nodes[i]
        onnx_node = onnx_graph.node_map.get(name)
        onnx_node.activation = act
