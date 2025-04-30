## mindspeed适配器
原有的llm_ptq模块主要支持基于transformers框架下的大模型量化压缩功能，本模块提供了针对modellink模型的量化适配器，可以直接量化mindspeed-LLM模型

### 前提条件
- 仅支持在以下产品中使用。
    - Atlas 训练系列产品。
    - Atlas A2训练系列产品/Atlas 800I A2推理产品。

- 已参考环境准备，完成CANN开发环境的部署、以及PyTorch 2.1.0及以上版本的框架和npu插件、Python环境变量配置。
- 大模型量化工具须执行命令安装如下依赖。
  如下命令如果使用非root用户安装，需要在安装命令后加上--user，例如：pip3 install onnx --user。
```
pip3 install numpy==1.25.2
pip3 install transformers        #需大于等于4.29.1版本，LLaMA模型需指定安装4.29.1版本
pip3 install accelerate==0.21.0  #若需要使用NPU多卡并行方式对模型进行量化，需大于等于0.28.0版本
pip3 install tqdm==4.66.1
```
- 安装mindspeed-LLM库,[安装指导](https://gitee.com/ascend/MindSpeed-LLM/blob/master/docs/features/install_guide.md)

### 功能约束
当前模型适配器仅验证过支持w8a8的量化，以及异常值抑制模块的m3和m5算法，仅支持NPU执行量化，不支持CPU量化

### 量化步骤（以llama2-7b legacy为例）
1.获取开源权重，转化为MindSpeed-LLM支持的模型,可以使用mindspeed-llm的权重[转化脚本](https://gitee.com/ascend/MindSpeed-LLM/blob/master/convert_ckpt.py)，[此处有转化脚本使用教程](https://gitee.com/ascend/MindSpeed-LLM/blob/master/docs/features/checkpoint.md)
```
python convert_ckpt.py \
    --model-type GPT \
    --load-model-type hf \
    --save-model-type mg \
    --target-tensor-parallel-size 1 \
    --target-pipeline-parallel-size 1 \
    --load-dir ./model_from_hf/llama-2-7b-hf/ \
    --save-dir ./model_weights/llama-2-legacy/ \
    --tokenizer-model ./model_from_hf/llama-2-7b-hf/tokenizer.model \
    --model-type-hf llama2
```
2.设计量化函数, 以w8a8为例：
```
def quant(model):
    # 准备校准数据，请根据实际情况修改，W8A16 Label-Free模式下请忽略此步骤
    dataset_calib = [["中国的首都在哪里？"],
                ["请做一首诗歌："],
                ["我想要学习python，该怎么学习？"]]

    from msmodelslim.pytorch.mindspeed_adapter import ModelAdapter, CalibratorAdapter, Linear    # 导入量化配置接口
    from msmodelslim.pytorch.llm_ptq.llm_ptq_tools import QuantConfig
    #转化模型，适配mindspeed-llm
    model = ModelAdapter(model)
    # 配置回退层,此处以回退mlp.dense_4h_to_h为例
    disable_names = []
    from megatron.core.tensor_parallel import ColumnParallelLinear, RowParallelLinear
    for name, mod in model.named_modules():
        if isinstance(mod, Linear) and "mlp.dense_4h_to_h" in name:
            disable_names.append(name)
    # 量化配置，请根据实际情况修改
    # 使用QuantConfig接口，配置量化参数，并返回量化配置实例
    quant_config = QuantConfig(
        w_bit=8,  
        a_bit=8,         
        disable_names=disable_names, 
        dev_type='npu',   # 在cpu进行量化时，需配置参数dev_type='cpu'，并取消参数dev_id=model.device.index的配置
        mm_tensor=False
    )  
    #使用CalibratorAdapter接口，输入加载的原模型、量化配置和校准数据，定义校准
    calibrator = CalibratorAdapter(model, quant_config, calib_data=dataset_calib, disable_level='L0')  
    calibrator.run()     #使用run()执行量化
    calibrator.save('./quant_weight', save_type=[ 'numpy', 'safe_tensor'])      #使用save()保存模型量化参数，请根据实际情况修改路径
    print('Save quant weight success!')
```

3.将上述量化函数插入推理脚本，以mindspeed-llm的自带推理精度测试脚本[evaluation.py](https://gitee.com/ascend/MindSpeed-LLM/blob/master/evaluation.py)为例，将quant函数插入main函数
```
 ...
def main():
    initialize_megatron(extra_args_provider=add_text_generate_args,
                        args_defaults={'no_load_rng': True,
                                       'no_load_optim': True})
    args = get_args()
    model = MegatronModuleForCausalLM.from_pretrained(
        model_provider=model_provider,
        pretrained_model_name_or_path=args.load, 
        local_files_only=True
    )
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name_or_path, trust_remote_code=True, local_files_only=True)
    quant(model) #插入之前写好的量化函数
    rank = dist.get_rank()
    if 'mmlu' in args.task:
        a = time.time()
        mmlu(args, LLMChat(args, model, tokenizer))
        if rank == 0:
            logger.info(f'MMLU Running Time:, {time.time() - a}')
 ...

```

4. 修改mindspeed-llm推理[脚本](https://gitee.com/ascend/MindSpeed-LLM/blob/master/examples/legacy/llama2/evaluate_llama2_7B_ptd.sh)执行上述量化，以legacy启动为例，修改脚本模型路径
```
 ...
 TOKENIZER_PATH=./model_from_hf/llama-2-7b-hf/  #huggingface开源模型路径
 CHECKPOINT=./model_weights/llama-2-legacy/  #前面转化生成的权重路径
 ...
 python -m torch.distributed.launch $DISTRIBUTED_ARGS evaluation.py   \
 ...
 --tensor-model-parallel-size 1  \
 --pipeline-model-parallel-size 1  \
 --padded-vocab-size 32000 \ #根据模型配置相应的模型参数
 ...
```
5.执行推理脚本，完成量化，进行伪量化精度验证
```
bash examples/legacy/llama2/evaluate_llama2_7B_ptd.sh
```