# 可选 LoRA：后端能力、授权与基准评估（v0.19）

> 合并原 `MODEL_ADAPTER_LAYER.md`、`FIND_LORA_PROTOCOL.md`、`LORA_LICENSE_AND_DOWNLOAD_GATE.md`、`LORA_BENCHMARK.md`。**LoRA 是可选增强，Reference/Style Pack 才是设计依据。** 当前仓库不包含模型权重，也不保证所用生图后端支持用户 LoRA。

## 1. 必须先判断是否可用

先读取 [model_adapters/backend_capabilities.json](../model_adapters/backend_capabilities.json) 或运行时可信能力声明：`backend_id`、`base_model_family/id/revision`、`supports_external_lora`、`supports_reference_images`、`supports_seed`、`supports_local_files`、`supports_weight_setting`、`max_loras` 等。unknown 不等于 yes。后端无外部 LoRA 接口、底模不确定、用户不允许联网或本风格不适用 → **`BASELINE_ONLY` / SKIP**，照常使用无 LoRA 的参考引导路线。

**不可假定 ChatGPT 内置生图接口支持加载第三方 .safetensors。**

## 2. 搜索只查元数据，不默认下载

仅在支持且确有价值时从可信模型卡/托管方查 3–5 个候选（[scripts/find_lora.py](../scripts/find_lora.py) 仅检索公开元数据；[scripts/lora_gate.py](../scripts/lora_gate.py) 只检查兼容及许可）。记录：作者与模型页 URL、revision、权重文件、大小、精确 base family/id、输出与商业/再分发许可、触发词、预览图、适用场景、风险。缺合法来源、精确许可、兼容性 → `REJECT_UNKNOWN` / `REJECT_UNVERIFIED`，不把授权请求当作跳过查证的方式。

筛选优先：后端支持/底模架构匹配/权重格式与许可证硬过滤；软比较参考媒介 30%、主体适配 20%、素材适配 15%、色彩表面稳定 15%、多样性 10%、成本性能 10%。没有实际预览的候选不能提升为 approved。

## 3. 下载断点与安全

仅对具名候选逐个向用户说明来源、许可证、用途、预计大小、费用、目标目录、拒绝后的 baseline 方案；收到本次明确批准才可由受信任环境下载。以 .safetensors 为首选，固定 revision 并校验 SHA256；不得执行陌生 install.sh、remote code、pickle/checkpoint。许可“允许访问”不等于允许商业或权重再分发；还需核实底模自身限制。仓库及分享 ZIP 默认不打包第三方模型权重。

## 4. 实测才可启用

进行 baseline/no-LoRA 与 LoRA 在尽量相同 Brief、尺寸、参考、底模和 seed（后端支持时）下的 paired A/B，至少 **3 种不同活动 × 2 variations**；对照图审视视觉媒介忠实度、风格收益、生成主体、结构多样性与成本。需至少 **2/3 活动明确受益**、无参考/字体硬失败，才可登记 promoted；否则记录 experimental/rejected，并退回 BASELINE_ONLY。

每次真正使用必须记录 `used_lora`、仓库/revision、scale、种子/参数、许可与可见证据；不能因为“看上去更漂亮”就覆盖 Lead DNA。默认最多一个 LoRA；混用需要独立测试。
