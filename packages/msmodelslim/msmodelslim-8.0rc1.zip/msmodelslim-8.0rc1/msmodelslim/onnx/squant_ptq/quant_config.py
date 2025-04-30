# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from ascend_utils.common.security.type import check_int, check_number, check_type
# quant_mode
# 0 : data-free
# 1 : label-free
QUANT_MODE_LIST = [0, 1]

# act_method
# 0 : data-free
# 1 : min-max
# 2 : histogram
ACT_METHOD_LIST = [0, 1, 2]
QUANT_PARAM_OPS_LIST = ['Conv', 'Gemm', 'MatMul']


class QuantConfig:
    """ The configuration for squant post training quant."""

    def __init__(
            self,
            w_bit=8,
            a_bit=8,
            w_signed=True,
            a_signed=False,
            w_sym=True,
            a_sym=False,
            input_shape=None,
            act_quant=True,
            act_method=0,
            quant_mode=0,
            disable_names=None,
            amp_num=0,
            squant_mode='squant',
            keep_acc=None,
            sigma=25,
            is_fp=False,
            disable_first_layer=True,
            disable_last_layer=True,
            is_optimize_graph=True,
            is_dynamic_shape=False,
            use_onnx=True,
            num_input=0,
            quant_param_ops=None,
            atc_input_shape=None,
            graph_optimize_level=0,
            shut_down_structures=None,
            device_id=0,
            om_method='aoe'
    ):
        # Basic setting
        self.w_bit = w_bit
        self.a_bit = a_bit
        self.w_signed = w_signed
        self.a_signed = a_signed
        self.w_sym = w_sym
        self.a_sym = a_sym
        if input_shape is None:
            input_shape = []
        self.input_shape = input_shape
        self.act_quant = act_quant
        self.sigma = sigma
        # name list for disabled modules
        if disable_names is None:
            disable_names = []
        self.disable_names = disable_names
        # number of layers for AMP fallback
        self.amp_num = amp_num
        # SQuant related
        self.squant_mode = squant_mode
        atc_input_shape = "" if atc_input_shape is None else atc_input_shape
        # Keep accuracy control, [bool, int] or bool
        # admm is for data-free/label-free, easy_quant is for data-free
        # round_opt is for label-free
        if quant_param_ops is None:
            self.quant_param_ops = ['Conv', 'Gemm', 'MatMul']
        else:
            self.quant_param_ops = quant_param_ops
        if keep_acc is None:
            self.keep_acc = {'admm': [False, 1000], 'easy_quant': [False, 1000], 'round_opt': False}
        else:
            self.keep_acc = keep_acc

        # act_method
        # 0 : squant
        # 1 : min-max
        # 2 : histogram
        self.act_method = act_method
        # quant_mode
        # 0 : data-free
        # 1 : label-free
        self.quant_mode = quant_mode

        # in label-free mode, act_method can't set to 0
        self.act_method = 1 if self.quant_mode == 1 and self.act_method == 0 else act_method

        self.is_fp = is_fp
        self.disable_first_layer = disable_first_layer
        self.disable_last_layer = disable_last_layer
        self.is_optimize_graph = is_optimize_graph
        self.is_dynamic_shape = is_dynamic_shape
        self.use_onnx = use_onnx
        self.num_input = num_input
        self.atc_input_shape = atc_input_shape
        self.aok_configuration(device_id, graph_optimize_level, om_method, shut_down_structures)

        self._check_params()

    def aok_configuration(self, device_id, graph_optimize_level, om_method, shut_down_structures):
        import acl

        self.graph_optimize_level = graph_optimize_level
        if shut_down_structures is None:
            shut_down_structures = []
        self.shut_down_structures = shut_down_structures
        self.arch = None
        self.opset_version = None
        soc_version = acl.get_soc_name()
        check_number(self.graph_optimize_level, int, 0, 2, param_name="graph_optimize_level")

        supported_soc_versions = ['Ascend310P3', 'Ascend310P5', 'Ascend310P7']
        if self.graph_optimize_level > 0:
            if soc_version in supported_soc_versions:
                self.soc_version = soc_version
            else:
                raise ValueError(
                    'Because of aok optimization, the soc_version should be one of '
                    f'{supported_soc_versions}'
                )
                
        self.iterations = 100
        self.runs = 1
        self.device_id = device_id
        self.om_method = om_method
        self.check_model = False
        self.debug = False
        self.check_output_threshold = None

    def _check_keep_acc_params(self):
        if 'admm' not in self.keep_acc:
            raise ValueError("admm should be in keep_accuracy")
        if 'easy_quant' not in self.keep_acc:
            raise ValueError("easy_quant should be in keep_accuracy")
        if 'round_opt' not in self.keep_acc:
            raise ValueError("round_opt should be in keep_accuracy")

    def _check_squant_mode(self):
        squant_mode_list = ['squant', 'squant-e', 'squant-k', 'squant-c']
        if self.squant_mode not in squant_mode_list:
            raise ValueError("squant_mode should be in "
                             "['squant', 'squant-e', "
                             "'squant-k', 'squant-c']")

    def _check_aok_params(self):
        check_type(self.shut_down_structures, list, param_name="shut_down_structures")
        check_type(self.device_id, int, param_name="device_id")
        om_method_list = ['atc', 'aoe']
        if self.om_method not in om_method_list:
            raise ValueError("om_method should be in ['atc', 'aoe']")

    def _check_params(self):
        if not isinstance(self.w_bit, int) or self.w_bit != 8:
            raise TypeError("w_bit must be 8, please check it.")
        if not isinstance(self.a_bit, int) or self.a_bit != 8:
            raise TypeError("a_bit must be 8, please check it.")
        check_type(self.is_fp, bool, param_name="is_fp")
        check_type(self.disable_first_layer, bool, param_name="disable_first_layer")
        check_type(self.disable_last_layer, bool, param_name="disable_last_layer")
        check_type(self.is_optimize_graph, bool, param_name="is_optimize_graph")
        check_int(self.amp_num, min_value=0, param_name="amp_num")
        check_type(self.sigma, int, param_name="sigma")
        if self.sigma != 0 and self.sigma != 25:
            raise ValueError("sigma should be 0 or 25")
        check_type(self.disable_names, list, param_name="disable_names")
        check_type(self.input_shape, list, param_name="input_shape")
        check_type(self.act_quant, bool, param_name="act_quant")
        check_type(self.w_signed, bool, param_name="w_signed")
        check_type(self.a_signed, bool, param_name="a_signed")
        check_type(self.w_sym, bool, param_name="w_sym")
        check_type(self.a_sym, bool, param_name="a_sym")
        check_type(self.is_dynamic_shape, bool, param_name="is_dynamic_shape")
        check_type(self.use_onnx, bool, param_name="use_onnx")
        check_type(self.num_input, int, param_name="num_input")
        check_type(self.atc_input_shape, str, param_name="atc_input_shape")
        check_type(self.quant_param_ops, list, param_name="quant_param_ops")

        if self.act_method not in ACT_METHOD_LIST:
            raise ValueError("act_method is invalid, please check it.")
        if self.quant_mode not in QUANT_MODE_LIST:
            raise ValueError("quant_mode is invalid, please check it.")
        if [False for elem in self.quant_param_ops if elem not in QUANT_PARAM_OPS_LIST]:
            raise ValueError("quant_param is invalid, please check it.")
        self._check_keep_acc_params()
        self._check_squant_mode()
        self._check_aok_params()
