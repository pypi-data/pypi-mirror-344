# -*- coding: utf-8 -*-
# Copyright Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from msmodelslim.onnx.squant_ptq.aok.optimizer.optimizations import AbstractOptimization
from msmodelslim.onnx.squant_ptq.aok.optimizer.transformations.abstract_transformation import AbstractTransformation
from msmodelslim.onnx.squant_ptq.aok.optimizer.optimizations.single_transform_optimization import \
    SingleTransformOptimization
from msmodelslim.onnx.squant_ptq.aok.optimizer.transformations import conv
from msmodelslim.onnx.squant_ptq.aok.optimizer.transformations import gelu


class DeleteConcatOptimization(AbstractOptimization):

    def get_simple_name(self) -> str:
        return 'DeleteConcat'

    def _setup_transformations(self, op_version: int) -> [AbstractTransformation]:
        return [
            conv.DoubleFuseBatchNormTransformation(op_version=op_version),
            gelu.ReplaceLeakyReluTransformation(op_version=op_version),
            conv.DeleteConcatTransformation(op_version=op_version),
        ]


class DoubleFuseBatchNormOptimization(AbstractOptimization):

    def get_simple_name(self) -> str:
        return 'DoubleFuseBn'

    def _setup_transformations(self, op_version: int) -> [AbstractTransformation]:
        return [
            conv.DoubleFuseBatchNormTransformation(op_version=op_version),
            gelu.ReplaceLeakyReluTransformation(op_version=op_version)
        ]


class FuseBatchNormOptimization(SingleTransformOptimization):

    def __init__(self) -> None:
        super(FuseBatchNormOptimization, self).__init__(conv.SingleFuseBatchNormTransformation)

    def get_simple_name(self) -> str:
        return 'FuseBn'


class PatchMerging2ConvOptimizationV0(SingleTransformOptimization):

    def __init__(self):
        super(PatchMerging2ConvOptimizationV0, self).__init__(conv.PatchMerging2ConvTransformationV0)

    def get_simple_name(self) -> str:
        return 'PatchMerging2ConvV0'


class PatchMerging2ConvOptimizationV1(SingleTransformOptimization):

    def __init__(self):
        super(PatchMerging2ConvOptimizationV1, self).__init__(conv.PatchMerging2ConvTransformationV1)

    def get_simple_name(self) -> str:
        return 'PatchMerging2ConvV1'


class PatchMerging2ConvOptimizationV2(SingleTransformOptimization):

    def __init__(self):
        super(PatchMerging2ConvOptimizationV2, self).__init__(conv.PatchMerging2ConvTransformationV2)

    def get_simple_name(self) -> str:
        return 'PatchMerging2ConvV2'


class PatchMerging2ConvOptimizationV3(SingleTransformOptimization):

    def __init__(self):
        super(PatchMerging2ConvOptimizationV3, self).__init__(conv.PatchMerging2ConvTransformationV3)

    def get_simple_name(self) -> str:
        return 'PatchMerging2ConvV3'


class ReplaceReshapeTransposeOptimizationV1(SingleTransformOptimization):

    def __init__(self) -> None:
        super(ReplaceReshapeTransposeOptimizationV1, self).__init__(conv.ReplaceReshapeTransposeTransformationV1)

    def get_simple_name(self) -> str:
        return 'ReplaceReshapeV1'


class ReplaceReshapeTransposeOptimizationV2(SingleTransformOptimization):

    def __init__(self) -> None:
        super(ReplaceReshapeTransposeOptimizationV2, self).__init__(conv.ReplaceReshapeTransposeTransformationV2)

    def get_simple_name(self) -> str:
        return 'ReplaceReshapeV2'


class ReplaceReshapeTransposeOptimizationV3(SingleTransformOptimization):

    def __init__(self) -> None:
        super(ReplaceReshapeTransposeOptimizationV3, self).__init__(
            conv.ReplaceReshapeTransposeTransformationV3
        )

    def get_simple_name(self) -> str:
        return 'ReplaceReshapeV3'


class Resize2ConvTransposeOptimization(SingleTransformOptimization):

    def __init__(self):
        super(Resize2ConvTransposeOptimization, self).__init__(conv.Resize2ConvTransposeTransformation)

    def get_simple_name(self) -> str:
        return 'Resize2ConvTranspose'
