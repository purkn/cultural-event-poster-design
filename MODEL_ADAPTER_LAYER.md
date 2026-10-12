# Model Adapter Layer — runtime design

## 核心观点
Reference → **设计**；Style Pack → **风格路由与语法**；LoRA → **生成时的视觉特征偏置**；HTML/CSS → **事实文字排版**。
LoRA 不是让普通标题自动变“艺术字”的快捷键，不保证主体比例、配色和构图；不能替换 Lead 视觉世界。

## 为什么默认不打包权重
- 第三方权重的许可证可能不允许再分发；使用权与重分发权分开检查。
- 文件体积大、模型更新快、不同基础架构不兼容；打包会使 Skill 不可维护。
- 很多托管图像生成工具不暴露外部 LoRA 加载能力，打包也没用。
- 团队成员共享轻量元数据/来源/基准报告即可，各自在获授权环境缓存。

## Backend Capability Probe（最高优先级）
至少确认 `backend_id`、`base_model_family`、`base_model_id/revision`、`supports_external_lora`、`supports_img2img`、`supports_seed`、`supports_reference_images`、`supports_weight_setting`、`supports_local_files`、`max_loras`。
- 不知道 = unknown；unknown 等同 LoRA 不可用，禁止假想加载接口。
- ChatGPT 内置的生图入口不能假定能加载用户自己选的 LoRA；需要确实可配置的外部执行后端（如受支持的 Diffusers/ComfyUI 工作流），并以实际接口为准。
- base family 只匹配“SDXL”还不够，若 candidate 需要特定衍生底模也须检查。

## 生命周期
`candidate → discovered → metadata_verified → consent_pending → approved → downloaded_verified → benchmarked → promoted | rejected`。
每个状态记录时间、证据 URL、文件 hash、底模 revision、适用 style_pack、已知失败、评分与使用许可。
Registry 最初为空；不得造一个“已测试过”的 LoRA。

## 风格包注入
每个 Style Pack 可附 `adapter_preferences.yaml`：
`dependency: discouraged | optional | preferred`，以及媒介适配任务与禁止任务。
**这不是候选权重名单；所有真正模型必须经 registry 的兼容/许可门禁。**

## 生成约束
默认一次启用一个 adapter；LoRA 混用需要独立验证，不能擅自累加。权重 `scale` 由候选模型卡建议和基准结果确定，不统一硬写 0.8。
输出记录：`used_lora: false | true` + exact model/revision/scale + baseline comparison evidence。
