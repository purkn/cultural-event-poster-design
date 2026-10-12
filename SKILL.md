---
name: cultural-event-poster-system
version: 0.19
description: 多风格自动文化活动海报生成；新增多路线 Prompt Compiler v0.17 / 否决反馈路由，并保留活动信息断点、LoRA 能力探针及中文字体门禁。优先遵从参考图空间、媒介、配色与字体人格。
---

# Cultural Event Poster System v0.19 — 运行规则

**交付目标**：从活动 brief + 可选素材 + 参考库生成完整海报；自动化设计执行，仅对真实缺口、权限与成本触发用户断点。
不要把“需要断点”理解为每一步都问用户选择方案。

## 唯一权威流水线（v0.17）
`A. BRIEF PREFLIGHT → [BP_CONTENT] → B. ASSET AUDIT → C. USER FEEDBACK REGISTRY & REJECTED ROUTE CHECK → D. REFERENCE RETRIEVAL / VISUAL EVIDENCE → E. >=2 DIFFERENT DESIGN ROUTES → F. BACKEND CAPABILITY / OPTIONAL LORA GATE → G. PROMPT COMPILER V017 → H. ROUTE ROUGHS → I. EARLY VISUAL COMPARISON / REJECT / REROUTE → J. H0 PROOFS → K. SVG-FIRST 双语排版（HTML 可选预览）→ L. FINAL RENDER + COMPOSITE READABILITY AUDIT / CONTROLLED REPAIR / RE-RENDER → M. INDEPENDENT DESIGN+PRODUCTION QC + VISUAL APPROVAL → FINAL`。

**最新用户审美否定优先于所有历史 Design PASS，自评 87/95 不可抵消用户反馈。** 先读 `ROUTE_RESELECTION_V017.md`、`PALETTE_AND_TYPE_DECISION_V017.md`、`VISUAL_QA_AND_SHORTCUT_AUDIT_V017.md`。v0.16 旧示例不再存在于运行时模块；每轮都必须构造新生产输入。

### 一、活动内容前置检查（不得跳过）
按 `BRIEF_INTAKE_BREAKPOINTS.md` 和 `scripts/preflight_brief.py` 执行，记录每个字段的来源与 confirmed/draft/missing 状态。
- **致命缺口**：正式海报的活动名、活动时间、实体活动的地点、线上活动的访问方式、已要求展示却缺失的票价/报名资料、必需的官方名称；先停下询问，严禁编造。
- 真实不存在的可选字段（logo、赞助方、场景图）不是默认停机理由。logo 缺失可推荐文字署名；主视觉素材缺失可由 AI 创作。
- 用户明确要求 teaser 且允许 `TBA` 才能不显示日期/地点；不得暗自决定。
- 中英正式名称与日期在输出前做双语逐项对照。需要官方译名时先确认；一般说明文案可起草并标注草拟。
- 多个相互独立的缺口合并询问，一次一组；先说明推荐处理路径。

### 二、Reference 核心不可被 LoRA 覆盖
继续遵守 v0.13 的 Lead Validity / Lead Dominance / Blueprint / Surface Fidelity / Typography Fidelity / Delta 门禁。
参考图决定 topology、明度、色彩角色、媒介、H0 人格、图文关系；LoRA 只负责**在已锁定的生成目标中稳定特定画面语言**。不能因为候选 LoRA 漂亮就改变风格路由。

### 三、LoRA Branch（可选，必须先检测后端）
1. 读取 `model_adapters/backend_capabilities.json` 或运行时明确的 backend 能力；不能假定通用生图 API 支持用户上传权重。
2. `supports_external_lora=false|unknown` → **直接 NO_LORA**，回到 reference-guided 基线生成；可在结果里说明未启用。不得声称已使用 LoRA。
3. 支持且画面媒介要求清晰 → 检查已获许可/通过基准测试的 registry。没有适合才启动 `find_lora`，优先候选元数据 + 预览，不自动下载。
4. 证实精确 base_model_family、版本/架构、权重格式、许可证、来源、用途权限之后才能提交下载建议；未知许可证或疑似不兼容 → 禁止下载。
5. **下载模型前必须显式询问用户，列明模型名、来源、大小、兼容底模、权限/费用、用途、保存位置、是否复用。用户可拒绝。**不同 LoRA 不能共用一个笼统的授权。
6. 同意后由具备该能力的受信任运行环境下载 safetensors 权重；校验来源与哈希，严禁执行仓库脚本 / remote code / pickle checkpoint。
7. LoRA 必须与不使用 LoRA 的 baseline 用相同 brief、seed（若后端支持）、尺寸、参考和采样参数做盲比；提升不明显或导致 Reference Delta RED → 关掉 LoRA。
8. 实测通过后只写入本地 registry metadata + 可选缓存路径；不把权重默认打进 Skill 发布包。

详见 `MODEL_ADAPTER_LAYER.md`、`FIND_LORA_PROTOCOL.md`、`LORA_BENCHMARK.md`、`LORA_LICENSE_AND_DOWNLOAD_GATE.md`。

### 三点五、v0.17 Prompt Compiler（替换 v0.16）
**必须执行** `modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md` 和 `scripts/compile_routes_v017.py`。不能把旧发酵节示例当默认值；收到「还是这个丑配色/字体」反馈要先重选路线，至少两条独立候选，若没选出来返回 `NEED_NEW_ROUTE`，不允许继续一条路线的 A/B/C 微调。
- `reference` 图像没真正传入后端时诚实标记 `TEXT_ONLY_REFERENCE_FALLBACK`，不要自称强参考生成。
- `feedback_registry` 项目级否定必须前置生效；技术正确不代表设计合格。
- LoRA 保留，可用则受许可证/授权/兼容检测控制，不可用就 `BASELINE_ONLY`。
- 没有看实际输出图不得打“Design PASS”，用户否定优先级最高。

### 四、v0.15 中文字体硬门禁（跨风格，必须执行）
**先读 `TYPOGRAPHY_ENGINE_V015.md` 与 `TYPE_SPECIMEN_SOP.md`，它们高于所有旧版本“字体推荐文字规则”。**
- 不可把“参考定制汉字”直接归纳成 Songti Light 然后用 CSS 放大；必须将 Lead 的逐字字形结构写入 Type Blueprint。
- 每个正式中文 H0 进入排版前必须知道真实字体文件路径、具体 face、全字符 cmap 覆盖、许可证状态与样张对比结果；不能凭 `font-family` 字符串判断已使用该字体。
- 产出本地字形样张并和 Lead H0 并排审美比较；如果 Lead 是强定制字且本地字体不匹配，触发 CUSTOM_DISPLAY 分支或 BP_FONT_DOWNLOAD，不允许静默回退普通系统字体。
- 若实际 HTML/CSS 不可用或无法复现字体选择，则技术检查标为 `UNVERIFIED`，不得自称“字体技术 PASS”。
- 中文与英文分别取证，中文错字/简繁误用/缺字/字面失配/过度松散竖排触发 H0 fail，Design / Production 两轴分别拦截。
- 同一海报可以不通过 LoRA 继续生成；但不能绕过中文字体门禁继续自评 85+。

### 五、H0 / 排版 / 输出
**v0.18 强制覆盖**：先读 `layout_engine_v018/SVG_FIRST_LAYOUT.md`、`layout_engine_v018/H0_VARIATION_GUARD.md` 和 `layout_engine_v018/README.md`。默认 H0 是 `STANDARD_BLOCK` 完整文字组合；无 Lead 逐字形变证据及验证路径时，禁止逐字缩放/旋转/大小变奏。最终可编辑源文件为 SVG + JSON Poster Plan；HTML 不再是唯一母版。一次局部排版返工后仍不合格，返回布局阶段，而非不断挪字。
- v0.13 政策继续有效：**H0 必须经过设计，但不必每种风格都发光/渐变/手绘**；根据 Lead 选择 REFERENCE_LED_DISPLAY_TYPE、GLYPH_SAFE_ARTWORD 或 IMAGE_INTEGRATED_H0。
- 日期/时间/地点/报名、票务、Logo 等信息通过 SVG `<text>` / SVG 对象进行精确排版；HTML/CSS 允许作为预览或复杂信息中间层，但必须共享同一 Poster Plan。AI 负责 Hero、特定艺术字或变形素材（且经文字核对）。
- 默认中英两版共享宏观布局，英文较长时只做局部布局适配；必须目检成图。
- 用户缺少资料时不要填虚构演出者、主办方、日期、场地或票价。
- 两轴评分保持：Design >=82、Production >=85；任何硬失败不得 PASS；评分必须以实图和对照证据为依据。

### 六、降级路径必须可追踪
- 资料不全且决定性 → WAITING_FOR_USER；不能把完成效果图作为正式交付。
- 当前后端不支持 LoRA → BASELINE_ONLY（**不属于失败**）。
- 无合规/兼容候选或用户拒绝下载 → BASELINE_ONLY，记录原因。
- 字体没下载授权 → 选已安装且符合字体人格的备选并说明。
- Reference 覆盖不足 → 使用 Coverage Gap，仍受通用设计质量门禁约束；不可编造“已比对某张图”。


### 六、v0.19 最终图文叠加可读性闭环（交付前必须执行）
**权威且唯一的可读性执行模块：** `layout_engine_v018/readability/README.md` + `layout_engine_v018/readability/audit_and_repair.py`。本模块位于 Svg Plan 组装之后、Production PASS 之前。`build_poster_svg.py` 直接导出的 PNG **仅是预览候选**，不得当最终成品。
1. 不仅检查字体/排版参数；必须实际渲染文字叠加后的**完整最终画面**，再从同一 SVG 分离 pre-text background 与具体文字层，局部逐像素检查。
2. 参照 WCAG 相对亮度：正文 >= 4.5:1、大字 >= 3:1；统计各字核心像素对比度第 10 百分位与达标比例 >=92%，并检测局部边缘复杂度、明度变化、主体标注保护区、25% 缩略视觉信号。只测全图平均明度或仅判断 text fill 不合格。
3. 自动修复严格按：位置（最多小幅偏移）→ 风格已批准色表 → 最小面积柔边底色处理（必须授权）→ 失败则布局整体重排。禁止默认黑蒙层、粗边描边、厚阴影。修复后**重新生成 SVG、重新渲染、重新测量**，最多 2 轮。
4. `technical_readability_gate=FAIL` 或 `must_escalate_layout=true` 时禁止交付，无论 Design/Production 评分多高；必须记录失败文字、bbox、局部对比、复杂度、修复动作及复检结果。
5. 技术指标通过**不自动等于视觉批准**：视觉代理必须实际检查最终 PNG 与 25% 视图、参考图图字关系、重要主体和 H0 字体，提供当前最终 PNG SHA256 的专门证据 JSON，调用 `--visual-review` 复验。未完成时状态 `VISUAL_REVIEW_PENDING`，不得报告正式 PASS。字体目标端与 CairoSVG 渲染不一致时继续标记未验证。
6. `protected_regions` 若缺失，算法不会虚构“已避开人物/重要物体”；这一步由可见图像的视觉复核补充。H0 必须是系统 SVG 文字或已核验定制路径，AI 位图伪字禁止承担正式信息。

## 有效规则索引
`ACTIVE_RULE_INDEX.md` 是唯一新旧版本冲突仲裁入口。新增模块优先于与其冲突的历史默认 LoRA/断点推断，不修改旧的参考风格约束。
