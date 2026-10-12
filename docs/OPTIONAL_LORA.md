# 可选 LoRA 后端与安全流程（v0.19）

LoRA 是可选的图像后端适配器，不替代 Lead 的构图、媒介、标题与色彩规则，也不构成生图必要依赖。当前仓库只有候选检索和门禁脚本，不附带模型权重、GPU 推理或端到端 LoRA 验证。

## 探测与降级
从 `model_adapters/backend_capabilities.json` 或当前运行时检验 backend_id、精确底模和 revision、外部 LoRA 支持能力、图像参考与权重加载能力。不支持或 unknown 直接 `BASELINE_ONLY`，不可假称已经使用 LoRA；不需要额外下载。

## 检索与授权
仅在后端明确支持且参考匹配需求确实受益时搜索 3–5 个候选；`scripts/find_lora.py` 仅获取元数据，`scripts/lora_gate.py` 只做离线兼容/许可检查。候选必须有作者、来源、权重版本和大小、精确底模、许可证原文或证据、商业与再分发权限、视觉预览。模糊或不兼容一律拒绝，不应向用户索要“未知风险授权”。

下载前单独征求当次、具名模型的用户同意，明确用途、大小、成本、保存位置与拒绝后的基线方案；不得执行外部仓库 install.sh、pickle 或远程代码，只接受可校验来源和哈希的受信任 safetensors。权重默认不进入分享 Skill 包。

## 真实对照与晋级
同 brief、seed（后端允许时）、尺寸、参考与采样参数比 baseline；至少 3 种 brief × 2 variations。须保留并排可见证据、模型 revision、adapter scale 和许可检查记录；至少 2/3 任务明显受益且没有 Lead 视觉 RED，才能在精确适用范围登记 promoted，否则 experimental/rejected。无实际推理绝不声称 LoRA 实测改善质量。
