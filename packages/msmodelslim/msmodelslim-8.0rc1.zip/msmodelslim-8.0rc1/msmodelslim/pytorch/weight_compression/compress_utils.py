# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.

import os 
import subprocess
import numpy as np 
from ascend_utils.common.security import safe_delete_path_if_exists, get_valid_write_path, SafeWriteUmask

 
def pseudo_sparse(arr, ratio):
    mask = np.random.choice([0, 1], size=arr.shape, p=[1 - ratio, ratio])
    arr = arr * mask
    return arr


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path, mode=0o750) 
    return path 


def compress_weight_fun(weights, record_detail_root='./'):
    shape_k, shape_n = weights.shape[:2]
    get_valid_write_path(record_detail_root, is_dir=True)
    write_root = makedirs(os.path.join(record_detail_root, str(os.getpid()), '.tmp'))
    try:
        input_weight_path = os.path.join(write_root, 'input_weight_path.bin')
        get_valid_write_path(input_weight_path)
        compress_output_path = os.path.join(write_root, 'compress_output.bin')
        get_valid_write_path(compress_output_path) 
        compress_index_path = os.path.join(write_root, 'compress_index.bin')
        get_valid_write_path(compress_index_path) 
        compress_info_path = os.path.join(write_root, 'compress_info.bin')
        get_valid_write_path(compress_info_path) 

        with SafeWriteUmask(umask=0o177):
            weights.astype(np.int8).tofile(input_weight_path)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        compress_excutor_path = os.path.join(current_dir, 'compress_graph', 'build', 'compress_excutor')
        command = '{} {} {} 1 1 1 0 0 {} {} {} {}'.format(compress_excutor_path, shape_k, shape_n, 
                            input_weight_path, compress_output_path, compress_index_path, compress_info_path)
        with SafeWriteUmask(umask=0o077):
            process = subprocess.Popen(command.split(), shell=False, stdout=subprocess.PIPE)
            process.wait(timeout=600)

        is_output_exist = os.path.exists(compress_output_path)
        is_index_exist = os.path.exists(compress_index_path)
        is_info_exist = os.path.exists(compress_info_path)
        if is_output_exist and is_index_exist and is_info_exist:
            output = np.fromfile(compress_output_path, dtype=np.int8)
            index = np.fromfile(compress_index_path, dtype=np.int8)
            info = np.fromfile(compress_info_path, dtype=np.uint32)
            result = list(info), output, index
        else:
            result = None, None, None
    except Exception as e:
        raise Exception("Error from compress function.", e) from e
    finally:
        tmp_dir = os.path.join(record_detail_root, str(os.getpid()))
        safe_delete_path_if_exists(tmp_dir, logger_level="debug")

    return result


def round_up(val, align):
    if align == 0:
        return 0
    return (val + align - 1) // align * align


def transform_nd2nz(nd_mat, block_size=(16, 32)):
    if not isinstance(block_size, (tuple, list)):
        raise ValueError('block_size is invalid, block_size should be a tuple or list')
    if len(block_size) != 2:
        raise ValueError('block_size should be a tuple or list with 2 elements')
    available_num = [16, 32]
    if block_size[0] not in available_num or block_size[1] not in available_num:
        raise ValueError('block_size is invalid, the elements in block_size should be {available_num}')

    r = round_up(nd_mat.shape[0], block_size[0])
    c = round_up(nd_mat.shape[1], block_size[1])
    r_pad = r - nd_mat.shape[0]
    c_pad = c - nd_mat.shape[1]
    nd_mat = np.pad(nd_mat, ((0, r_pad), (0, c_pad)))
    nz_mat = np.transpose(
        np.reshape(
            nd_mat, (
                r // block_size[0], block_size[0], c // block_size[1], block_size[1]
            )
        ), (2, 0, 1, 3)
    )
    return nz_mat
