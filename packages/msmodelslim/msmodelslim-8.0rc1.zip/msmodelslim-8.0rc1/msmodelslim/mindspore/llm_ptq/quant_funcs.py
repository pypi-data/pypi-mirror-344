# Copyright Huawei Technologies Co., Ltd. 2023-2024. All rights reserved.

import mindspore as ms
import mindspore.ops as P


def linear_quantize(input_tensor, scale, zero_point):
    # reshape scale and zeropoint for convolutional weights and activation
    if len(input_tensor.shape) == 4:
        scale = scale.view(-1, 1, 1, 1)
        zero_point = zero_point.view(-1, 1, 1, 1)
    # reshape scale and zeropoint for linear weights
    elif len(input_tensor.shape) == 2:
        scale = scale.view(-1, 1)
        zero_point = zero_point.view(-1, 1)
    # mapping single-precision input to integer values
    # with the given scale and zeropoint
    return input_tensor / scale + zero_point


def linear_dequantize(input_tensor, scale, zero_point):
    # reshape scale and zeropoint for convolutional weights and activation
    if len(input_tensor.shape) == 4:
        scale = scale.view(-1, 1, 1, 1)
        zero_point = zero_point.view(-1, 1, 1, 1)
    # reshape scale and zeropoint for linear weights
    elif len(input_tensor.shape) == 2:
        scale = scale.view(-1, 1)
        zero_point = zero_point.view(-1, 1)
    # mapping integer input to fixed point float point value
    # with given scaling factor and zeropoint
    return (input_tensor - zero_point) * scale


def fake_quantize(tensor,
                  scale,
                  zero_point,
                  bit=8):
    """ Fake quantization."""

    quant_tensor = linear_quantize(tensor, scale, zero_point)

    n = 2 ** (bit - 1)
    q_min, q_max = -n, n - 1

    quant_tensor = quant_tensor.round()

    quant_tensor = P.clamp(quant_tensor, q_min, q_max)

    dequant_tensor = linear_dequantize(quant_tensor, scale, zero_point).astype(ms.float16)

    return quant_tensor, dequant_tensor


def linear_quantization_params(
        bit,
        x_min,
        x_max,
):
    """Get scale and offset quantization params"""
    eps = P.Eps()(ms.Tensor(1.0)).astype(x_min.type())
    x_min = P.minimum(x_min, P.zeros_like(x_min))
    x_max = P.maximum(x_max, P.zeros_like(x_max))

    n = 2 ** bit - 1
    scale = (x_max - x_min) / n
    scale = P.maximum(scale, eps)
    zero_point = -1 * x_min / scale
    zero_point = zero_point.round()

    qmin = -1 * (2 ** (bit - 1))
    zero_point += qmin
    
    return scale, zero_point

    