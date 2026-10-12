# v0.11 Skill Hygiene & Shortcut Audit

## 结论
v0.10 没有发现恶意脚本、联网代码或临时垃圾文件，但存在**规则卫生**与**设计偷懒路径**问题。v0.11 已针对高风险项清理。

## 一、文件卫生问题
### 1. 版本漂移 — 已修
v0.10 包中同时存在：
- Core Architecture v0.9
- QA v0.9
- Genericness Penalty v0.7
- S01 STYLE v0.8
- 多个 core YAML v0.9

这会让 Agent 不知道哪份规则优先。
**修复**：主运行文档统一到 v0.11；增加 README 规则优先级；旧 V08/V09 诊断移入 `archive/diagnostics/`。

### 2. Style Pack 规范与实际结构不一致 — 已修
`STYLE_PACK_SPEC v2.1` 要求 hero grammar / artword grammar / typography / layout / evaluator / prompt compiler / anchors / tests，但 S01 实际缺失。
**修复**：S01 补齐这些文件与 regression tests。

### 3. 历史诊断污染运行路径 — 已修
V08/V09 诊断位于根目录，容易被误当现行协议。
**修复**：移入 archive；明确 archive 永不参与运行优先级。

### 4. Rough 数量冲突 — 已修
v0.10 的 route_competition 设 `rough_count_max: 2`，Coverage LOW 又要求 3 rough。
**修复**：动态 rough count；HIGH/MEDIUM >=2，LOW >=3。

## 二、偷懒捷径问题
### 1. Multi-reference Averaging — 高风险，已修
v0.10 默认 Reference Quartet / Role-based Synthesis，容易变成 A 色彩 + B 构图 + C 字体 + D 材质的无人格平均。
**修复**：Lead Reference First，默认 1 Lead + 0–1 Support。

### 2. Coverage Gap Mashup — 高风险，已修
v0.10 MEDIUM/LOW 会鼓励 multi-family synthesis。
**修复**：覆盖不足时先找结构最接近的 Lead；无 Lead 才 concept-led，且每张 rough 保持单一视觉人格。

### 3. Plain Font H0 — 高风险，已修
虽然 glyph-safe 文件禁止 plain-font fallback，但主运行规则未将其设为全局 Hard Gate。
**修复**：H0 Design Gate 全局化；普通字体放大/描边/字距不算艺术字。

### 4. Post-hoc Concept — 高风险，已修
过去可以先出普通图，再用“光/蒸汽/纹理”解释概念。
**修复**：Concept Embodiment + Removal Test；概念必须改变至少两个结构维度。

### 5. Safe Institutional Template — 高风险，已修
正式文化活动容易自动滑向米白、边框、大宋体、矩形图、三栏信息。
**修复**：新增 safe-template 组合惩罚；高风险组合不能靠信息清晰通过。

### 6. Technical QC Inflation — 高风险，已修
无水印、无溢出、信息正确会把总分抬到 80+。
**修复**：Design / Production 完全分开，两者均达标才可 PASS。

### 7. No-evidence Self Scoring — 高风险，已修
只看 prompt 或 HTML 就宣称视觉“在线”。
**修复**：没有目检最终图，Design 分上限 60；没有 Lead 并排比较，相关维度封顶。

### 8. One-Rough Shortcut — 已修
第一张“能用”就精修。
**修复**：正常至少 2 rough，LOW coverage 至少 3；仅 Strong Lead + 首稿 Design >=88 可例外。

### 9. Asset-as-is — 已覆盖并强化
素材默认先做 affordance 分析，除 PRESERVE 外不能直接贴版。

## 三、尚未完全解决的风险
1. 113 张 Reference Library 的分类仍是 provisional。发现 4 张低置信条目：`REF-027 / REF-067 / REF-093 / REF-102`，原 `cluster_reason` 为 `fallback; needs visual refinement`。v0.11 已在 index 中显式标记 `strong_lead_eligible=false`；其余条目也要求实际视觉检查后才可进入 Strong Lead。
2. 当前只有 1 个正式 Style Pack，Router 的跨风格能力仍需等后续 Style Pack 增加后回归测试。
3. H0 艺术字的高质量生成仍受图像模型中文字形能力影响，因此必须保留 glyph-safe hybrid。
4. “审美好坏”无法被规则完全形式化，因此 Evidence-based Critic 必须持续依赖真实视觉对比，而不是纯文本自证。

## 四、卫生检查结果
- `__MACOSX`: 无
- `.DS_Store`: 无
- 临时 `.tmp/.bak/.pyc`: 无
- 内嵌 zip: 无
- 可执行脚本: 无
- archive 与 active rules 已分离
