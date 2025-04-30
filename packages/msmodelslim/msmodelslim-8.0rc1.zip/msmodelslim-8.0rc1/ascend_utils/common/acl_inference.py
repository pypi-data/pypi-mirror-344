# Copyright Huawei Technologies Co., Ltd. 2022-2022. All rights reserved.

import time
from collections import namedtuple

import numpy as np

import acl
from ascend_utils.common.security import check_element_type, check_int, get_valid_read_path, MAX_READ_FILE_SIZE_32G
from msmodelslim import logger

ACL_ERROR_NONE = 0
ACL_MEM_MALLOC_HUGE_FIRST = 0

# memory copy code
ACL_MEMCPY_HOST_TO_DEVICE = 1
ACL_MEMCPY_DEVICE_TO_HOST = 2
IS_ACL_INITIALIZED_BY_THIS_MODULE = False  # False for acl being initialized out of this module

# data type map
ACL_DTYPE = {
    0: "float32",
    1: "float16",
    2: "int8",
    3: "int32",
    4: "uint8",
    6: "int16",
    7: "uint16",
    8: "uint32",
    9: "int64",
    10: "uint64",
    11: "float64",
    12: "bool",
}

NodeType = namedtuple("NodeType", ["name", "shape", "dtype", "size", "data_format"])


def _check_ret(message, ret):
    if ret != ACL_ERROR_NONE:
        raise Exception("{} failed ret = {}".format(message, ret))


def init_acl(device_id=0, config_path=None):
    global IS_ACL_INITIALIZED_BY_THIS_MODULE

    _, device_ret = acl.rt.get_device()
    if device_ret == 0:
        logger.info(f'acl already initialized')
    else:
        ret = acl.init(config_path) if config_path else acl.init()
        _check_ret("acl.init", ret)
        IS_ACL_INITIALIZED_BY_THIS_MODULE = True

    ret = acl.rt.set_device(device_id)  # set_device is actually not very effective
    _check_ret("acl.rt.set_device", ret)
    logger.info(f'acl set_device {device_id}')


def release_acl(device_id=0):
    global IS_ACL_INITIALIZED_BY_THIS_MODULE

    ret = acl.rt.reset_device(device_id)
    _check_ret("acl.rt.reset_device", ret)
    logger.info(f"end to reset device {device_id}")

    logger.info(f'release_acl, IS_ACL_INITIALIZED_BY_THIS_MODULE: {IS_ACL_INITIALIZED_BY_THIS_MODULE}')
    if not IS_ACL_INITIALIZED_BY_THIS_MODULE:  # Will finalize outside this module
        return

    ret = acl.finalize()
    _check_ret("acl.finalize", ret)
    logger.info("end to finalize acl")
    IS_ACL_INITIALIZED_BY_THIS_MODULE = False


class AclInference:
    """
    OM model inference with ACL interface.
    Note: Need to call `init_acl` and `release_acl` manually, as `acl.init` and `acl.finalize` not re-enterable.
    Note: This class is not used in msmodelslim directly, but for KIA usage.

    Example:
    >>> from ascend_utils.common import acl_inference
    >>> device_id = 0
    >>> acl_inference.init_acl(device_id=device_id)
    >>> mm = acl_inference.AclInference('resnet50.om', device_id=device_id)
    >>> output = mm(np.ones([1, 3, 224, 224]).astype('float32'))
    >>> print(output[0].shape)
    >>> # (1, 1000)
    >>> print(mm.get_execute_time())
    >>> # 0.8130073547363281
    >>> acl_inference.release_acl(device_id=device_id)
    """
    def __init__(self, model_path, device_id=0):
        check_int(device_id, min_value=0, param_name="device_id")
        self.model_path = get_valid_read_path(model_path, extensions=["om"], size_max=MAX_READ_FILE_SIZE_32G)
        self.device_id = device_id

        # Create a new context for each new model
        self.context, ret = acl.rt.create_context(device_id)
        _check_ret("acl.rt.create_context", ret)
        logger.info(f"end to create_context")

        self.model_id, ret = acl.mdl.load_from_file(self.model_path)
        _check_ret("acl.mdl.load_from_file", ret)

        self.model_desc = acl.mdl.create_desc()
        ret = acl.mdl.get_desc(self.model_desc, self.model_id)
        _check_ret("acl.mdl.get_desc", ret)

        self.inputs, self.outputs = self.get_inputs(), self.get_outputs()
        self.num_inputs, self.num_outputs = len(self.inputs), len(self.outputs)

        if self.num_inputs == 0 or self.num_outputs == 0:
            raise ValueError("model with zero input or output currently not supported")
        if self.inputs[-1].name == "ascend_mbatch_shape_data":
            raise ValueError("model with ascend_mbatch_shape_data currently not supported")
        if any([ii.shape is None for ii in self.outputs]):
            raise ValueError("model dynamic input or output currently not supported")

        self.input_data_buffer = self._init_input_device_buffer()
        self.output_data_buffer = self._init_output_device_buffer()
        self.output_host_bytes_data, self.output_host_buffer = self._init_output_host_buffer()
        self.execute_time_ms = 0  # Recording the latest executing time

    def __call__(self, input_data):
        acl.rt.set_context(self.context)
        cur_input_data = input_data if isinstance(input_data, (list, tuple)) else [input_data]
        check_element_type(cur_input_data, np.ndarray)
        if len(cur_input_data) != len(self.inputs):
            raise ValueError(
                "input data counts: {} not matching with model: {}".format(len(cur_input_data), len(self.inputs))
            )
        for cur_input, model_input in zip(cur_input_data, self.inputs):
            cur_shape, model_shape = list(cur_input.shape), list(model_input.shape)
            if cur_shape != model_shape:
                raise ValueError("input data shape {} not matching model input shape {}".format(cur_shape, model_shape))
            cur_dtype, model_dtype = cur_input.dtype, model_input.dtype
            if cur_dtype != ACL_DTYPE.get(model_dtype):
                raise TypeError("input data type {} not matching model input type {}".format(cur_dtype, model_dtype))

        load_input_dataset = self._input_data_from_host_to_device(cur_input_data)
        load_output_dataset = self._create_output_data_device_buffer()
        start = time.time()
        ret = acl.mdl.execute(self.model_id, load_input_dataset, load_output_dataset)
        self.execute_time_ms = (time.time() - start) * 1000
        _check_ret("acl.mdl.execute", ret)

        self._destroy_data_buffer(load_input_dataset)
        self._destroy_data_buffer(load_output_dataset)
        return self._output_data_from_device_to_host(output_shape=[ii.shape for ii in self.get_outputs()])

    @staticmethod
    def _init_acl_data_buffer(acl_dataset, data_buffer, data_size):
        data = acl.create_data_buffer(data_buffer, data_size)
        if data is None:
            ret = acl.destroy_data_buffer(acl_dataset)
            _check_ret("acl.destroy_data_buffer", ret)

        _, ret = acl.mdl.add_dataset_buffer(acl_dataset, data)
        if ret != ACL_ERROR_NONE:
            ret = acl.destroy_data_buffer(acl_dataset)
            _check_ret("acl.destroy_data_buffer", ret)

    @staticmethod
    def _destroy_data_buffer(dataset):
        if not dataset:
            return
        num = acl.mdl.get_dataset_num_buffers(dataset)
        for cur_id in range(num):
            data_buf = acl.mdl.get_dataset_buffer(dataset, cur_id)
            if data_buf:
                ret = acl.destroy_data_buffer(data_buf)
                _check_ret("acl.destroy_data_buffer", ret)
        ret = acl.mdl.destroy_dataset(dataset)
        _check_ret("acl.mdl.destroy_dataset", ret)

    def get_inputs(self):
        results = []
        input_size = acl.mdl.get_num_inputs(self.model_desc)
        for cur_id in range(input_size):
            data_dims, _ = acl.mdl.get_input_dims(self.model_desc, cur_id)
            data_format = acl.mdl.get_input_format(self.model_desc, cur_id)
            data_size = acl.mdl.get_input_size_by_index(self.model_desc, cur_id)
            data_type = acl.mdl.get_input_data_type(self.model_desc, cur_id)
            cur_node = NodeType(data_dims.get("name"), data_dims.get("dims"), data_type, data_size, data_format)
            results.append(cur_node)
        return results

    def get_outputs(self):
        results = []
        output_size = acl.mdl.get_num_outputs(self.model_desc)
        for cur_id in range(output_size):
            data_dims, _ = acl.mdl.get_output_dims(self.model_desc, cur_id)
            data_format = acl.mdl.get_output_format(self.model_desc, cur_id)
            data_size = acl.mdl.get_output_size_by_index(self.model_desc, cur_id)
            data_type = acl.mdl.get_output_data_type(self.model_desc, cur_id)
            data_name = acl.mdl.get_output_name_by_index(self.model_desc, cur_id)
            cur_node = NodeType(data_name, data_dims.get("dims"), data_type, data_size, data_format)
            results.append(cur_node)
        return results

    def get_execute_time(self):
        return self.execute_time_ms

    def release_resource(self):
        ret = acl.mdl.unload(self.model_id)
        _check_ret("acl.mdl.unload", ret)
        ret = acl.mdl.destroy_desc(self.model_desc)
        _check_ret("acl.mdl.destroy_desc", ret)
        for buffer in self.input_data_buffer:
            ret = acl.rt.free(buffer["buffer"])
            _check_ret("acl.rt.free", ret)
        for buffer in self.output_data_buffer:
            ret = acl.rt.free(buffer["buffer"])
            _check_ret("acl.rt.free", ret)

        # Also destroy context
        ret = acl.rt.destroy_context(self.context)
        _check_ret("acl.rt.destory_context", ret)
        logger.info(f"end to destroy_context")

    def _init_input_device_buffer(self):
        input_data_buffer = []
        for cur_id in range(self.num_inputs):
            temp_buffer_size = acl.mdl.get_input_size_by_index(self.model_desc, cur_id)
            temp_buffer, ret = acl.rt.malloc(temp_buffer_size, ACL_MEM_MALLOC_HUGE_FIRST)
            _check_ret("acl.rt.malloc", ret)
            acl.rt.memset(temp_buffer, temp_buffer_size, 0, temp_buffer_size)
            input_data_buffer.append({"buffer": temp_buffer, "size": temp_buffer_size})
        return input_data_buffer

    def _init_output_device_buffer(self):
        output_data_buffer = []
        for cur_id in range(self.num_outputs):
            temp_buffer_size = acl.mdl.get_output_size_by_index(self.model_desc, cur_id)
            temp_buffer, ret = acl.rt.malloc(temp_buffer_size, ACL_MEM_MALLOC_HUGE_FIRST)
            _check_ret("acl.rt.malloc", ret)
            acl.rt.memset(temp_buffer, temp_buffer_size, 0, temp_buffer_size)
            output_data_buffer.append({"buffer": temp_buffer, "size": temp_buffer_size})
        return output_data_buffer

    def _init_output_host_buffer(self):
        output_host_bytes_data, output_host_buffer = [], []
        for cur_id in range(self.num_outputs):
            temp_buffer_size = acl.mdl.get_output_size_by_index(self.model_desc, cur_id)
            bytes_data = np.empty((temp_buffer_size,), dtype="bool")
            bytes_data_ptr = bytes_data.__array_interface__["data"][0]
            output_host_bytes_data.append(bytes_data)
            output_host_buffer.append({"buffer": bytes_data_ptr, "size": temp_buffer_size})  # Same format as ACL one

        return output_host_bytes_data, output_host_buffer

    def _input_data_from_host_to_device(self, input_data):
        load_input_dataset = acl.mdl.create_dataset()
        for cur_id, (model_input, data_buffer, data) in enumerate(zip(self.inputs, self.input_data_buffer, input_data)):
            if not data.flags["C_CONTIGUOUS"]:
                data = np.ascontiguousarray(data)
            ptr = data.__array_interface__["data"][0]
            malloc_size = data.size * data.itemsize
            ret = acl.rt.memcpy(data_buffer["buffer"], malloc_size, ptr, malloc_size, ACL_MEMCPY_HOST_TO_DEVICE)
            _check_ret("acl.rt.memcpy", ret)

            self._init_acl_data_buffer(load_input_dataset, data_buffer["buffer"], data_buffer["size"])
            input_desc = acl.create_tensor_desc(model_input.dtype, list(data.shape), model_input.data_format)
            load_input_dataset, ret = acl.mdl.set_dataset_tensor_desc(load_input_dataset, input_desc, cur_id)
            if ret != ACL_ERROR_NONE:
                ret = acl.destroy_data_buffer(load_input_dataset)
                _check_ret("acl.destroy_data_buffer", ret)
        return load_input_dataset

    def _create_output_data_device_buffer(self):
        load_output_dataset = acl.mdl.create_dataset()
        for data_buffer in self.output_data_buffer:
            self._init_acl_data_buffer(load_output_dataset, data_buffer["buffer"], data_buffer["size"])
        return load_output_dataset

    def _output_data_from_device_to_host(self, output_shape):
        results = []
        for cur_id in range(self.num_outputs):
            ptr = self.output_host_buffer[cur_id]["buffer"]
            numpy_dtype = np.dtype(ACL_DTYPE.get(self.outputs[cur_id].dtype))
            data_len = int(np.prod(output_shape[cur_id])) if output_shape[cur_id] else 1
            malloc_size = data_len * numpy_dtype.itemsize
            ret = acl.rt.memcpy(
                ptr, malloc_size, self.output_data_buffer[cur_id]["buffer"], malloc_size, ACL_MEMCPY_DEVICE_TO_HOST
            )
            _check_ret("acl.rt.memcpy", ret)

            np_array = np.frombuffer(self.output_host_bytes_data[cur_id], dtype=numpy_dtype, count=data_len)
            results.append(np_array.reshape(output_shape[cur_id]))
        return results
