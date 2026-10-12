# find_lora — Search, Review, Select (NO DOWNLOAD BY DEFAULT)

## 输入
`style_pack_id`、目标参考图/Lead 指纹、medium/surface、期望主体类型、asset strategy、H0 strategy、target backend capabilities、usage (classroom/noncommercial/commercial)、是否允许外部搜索。

## Step 0（短路）
- backend 不支持第三方 LoRA、base model 未确定、用户禁止外网 → `SKIP`; 不消耗检索请求。
- LoRA 对该风格为 discouraged 或 Reference/图像编辑更适合 → `SKIP`。
- 已缓存且已验证 license/兼容+实测收益 → 可直接复用，无需重复下载（如变更用途/权限需重新审核）。

## Step 1（候选来源）
允许 Hugging Face 官方模型仓库 API、可信模型卡及用户指定来源；未知来源的下载页一律先审查。可用 `scripts/find_lora.py` 生成**候选元数据**，它不会下载权重。
每次只寻找 3–5 个强相关候选；用实际预览（作者 sample images / 使用说明）检查是否真的像 Lead。不可只靠搜索标题里的“editorial / poster / crayon”等词打分。

## Step 2（必填证据）
- 精确模型地址、作者/发布者、revision/commit、权重文件名和格式、size MB
- base_model_family + base_model_id + 必要的版本
- license 的具体名称、核验状态、模型卡或许可证证据链接、commercial/output/redistribution 权限（如需）与限制
- trigger words / recommended strengths，如果可验证
- NSFW / 侵权/人物版权风险按项目策略复核
- 视觉预览或可信测试图（至少 2 张）、是否和 Lead medium/value/type DNA 冲突
缺少关键项 = `REJECT_UNKNOWN`；不能靠“用户同意了”就默认许可证合法。

## Step 3（候选排序）
HARD FILTER: backend support / exact base / format / license / source / safe download.
SOFT RANK: 参考图媒介相似度 30%、实际主体适配 20%、已有素材适配 15%、颜色与表面稳定性 15%、多样性 10%、性能/成本 10%。缺视觉证据一律 provisional，不提升为 approved。

## Step 4（断点）
用户仅确认某个**具名** LoRA 的项目本地下载。信息必须包含用途、大小、托管方、版本、许可与拒绝替代方案。
同意后，使用支持的受信任下载器按精确版本获取 **.safetensors** 文件，校验 hash。严禁执行用户不熟悉仓库内脚本或加载不可信 pickle。

## Step 5（效果验收）
先做同种子 paired A/B，然后批量 3 briefs × 2 variations；可见提升且不牺牲 Lead Fidelity 才 promotion。详见 `LORA_BENCHMARK.md`。

## 自带工具的严格边界
- `scripts/find_lora.py`：公开 HF 模型元数据检索，**不下载** LoRA，环境无网时可用 `--offline` 回显现有 registry 候选。
- `scripts/lora_gate.py`：离线兼容与许可预检，只返回状态报告；不执行下载或推理。
- 下载是可选外部适配器动作：没有受信任下载工具或没有实际授权时不执行。
