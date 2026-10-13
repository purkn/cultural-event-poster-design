# 质量验收、图文可读性和正式交付

> 本文合并原 `QA_ACCEPTANCE.md`、`DESIGN_QUALITY_CORE.md` 中评分和证据要求。**数值以 [core/design_quality_scores.yaml](../core/design_quality_scores.yaml) 为权威；像素检测阈值以 [layout_engine/readability/audit_and_repair.py](../layout_engine/readability/audit_and_repair.py) 为执行权威**，详细说明见 [readability 模块](../layout_engine/readability/README.md)。

## 1. 先硬门禁，后分数

机械事实错误、H0 错字/错地区字形、Strong Lead 不成立、Blueprint 未保存、Support 篡改全局设计、Surface/Type/Palette/Delta RED、无依据的渐变/填充装饰、低质套模板、正式信息排版不可用，均不得正式交付。用户已经明确否定某稿，不能用自动评分覆盖。

Design ≥ **82/100**，Production ≥ **85/100**；两项不能互相补偿，技术通过不等于视觉设计通过。

| Design（共 100） | 分值 |
| --- | ---: |
| Concept 可见性 | 12 |
| Lead Blueprint 结构忠实度 | 12 |
| 媒介/表面忠实度 | 12 |
| H0/字体忠实度 | 12 |
| 图字融合 | 10 |
| 构图和视觉张力 | 10 |
| 色彩/明度结构 | 9 |
| 素材变化与应用 | 7 |
| 非模板感/效果纪律 | 6 |
| 信息架构 | 4 |
| 留白意图 | 3 |
| 主题专属性 | 3 |

| Production（共 100） | 分值 |
| --- | ---: |
| 事实准确 | 20 |
| H0 字符准确 | 15 |
| 可读性/溢出 | 15 |
| 信息完整 | 12 |
| 图像清洁 | 10 |
| 输出格式/分辨率 | 10 |
| 双语一致性 | 10 |
| 必须保留的素材 | 8 |

## 2. 证据优先于自评

- 未真实目检最终图：Design 上限 60；有 Lead 而缺 Structure/Surface/Typography Delta：Design 上限 70。
- 无 Surface Fingerprint 对应分项最多 4/12；无 H0 Type DNA 对应分项最多 4/12；无 Support Scope 却使用 Support：Design FAIL。
- 无真实字体文件来源/覆盖证据：`TYPE_GATE_TECH FAIL`；无 H0 标题参考裁片 + 候选字体样张 + 成图对照，字体设计分项最多按原规定 40% 计。两种语言独立核验。
- 无实际 rough / 无实际参考图视觉观察，不得凭合规文本得 Design PASS。风格不匹配应退回路线，不把纯技术指标算成审美。

### 评审机制：借鉴 Taste-Skill，按海报语境执行

采用 Taste-Skill 的 Brief Inference（§0）、反默认套路检查（§9）、先审计后修改（§11）和最终逐项预检（§14）。本仓库直接维护适用于海报的机制，不要求安装 Taste-Skill，也不复制其网页技术栈、动画参数、卡片布局、单强调色或字体/标点禁令。是否使用居中构图、宋体、纯黑、渐变和高密度，由活动、受众、品牌与 Lead 证据决定。

**先写 Design Read**：一句话说明“什么活动、给谁看、在哪个渠道/尺寸传播、期望什么视觉语言、参考依据是什么”。在 Concept Card 中描述构图变化程度与信息密度的选择及理由，避免直接套用固定数值。改已有海报时先列保留的事实、品牌、素材和视觉资产，再列需要修复的部分；未被要求改变的内容继续保留。

| 评审时机 | 实际检查与记录 | 失败返回 |
| --- | --- | --- |
| 生成前 | Design Read、素材使用、Lead 与 Concept 是否一致，是否沿用被拒绝路线 | Brief、参考或 Concept |
| Rough 后 | 两条真实不同路线与各自 Lead 并排；指出具体位置的结构、媒介、字体、配色差异，进行换题测试 | 主视觉或新路线 |
| 字体排版后 | H0 裁片与至少两套字形样张；原尺寸层级、字图关系和中英信息空间 | 字体或整体版式 |
| 最终交付前 | 当前最终 PNG、其 25% 缩略图、参考对照、字体证明、Blueprint、Poster Plan；逐项预检、双轴评分和问题复验 | 对应失败阶段 |

**评语必须能定位**：写“标题右下角与人物肩部重叠，缩略后日期失去层级”，并提出修复动作；不接受“很高级、符合规则、信息完整”作为审美依据。先修最影响阅读、概念和参考忠实度的问题，不能靠增添装饰或改分数掩盖问题。

**反默认套路检查**只提出疑点：无结构作用的主题符号、装饰标签/微文案、无参考依据的默认色板或字体、无必要效果与模板构图。每项标记 `ABSENT`、`JUSTIFIED` 或 `REWORK`，并提供画面证据；`JUSTIFIED` 需说明其 Brief/Lead 来源或结构职责。例如参考本来是纯黑大字居中，就应保留，而不是为了“反 AI”强迫换色和偏轴构图。

最终八项预检以 [core/universal_poster_critic.yaml](../core/universal_poster_critic.yaml) 为唯一清单：活动/受众适合度、参考忠实、可见概念与主题专属、字体与图字工艺、构图层级与密度、配色媒介一致性、事实与双语准确、输出及证据完整性。每项需具体观察及 `PASS/FAIL`，不靠平均分抵消失败项。

**问题闭环**：每个问题记录 `area/evidence/repair_action/status`；修复后记录复验观察及当前 `rechecked_render_sha256`。存在 OPEN、缺失复验或旧 SHA 的问题就不能正式 PASS。通常最多两轮局部审美修正；仍有结构性失败时回到 Concept/Lead/版式，自主准备新路线，不无限调整字号。此工作流建议不同于像素模块固定最多两轮自动修复。

### 可执行的最终评审协议

从 [visual_review_template.json](../layout_engine/readability/visual_review_template.json) 复制空模板到项目目录，在真实看图后填写：

- `render_sha256`、`reviewer`、`decision`；Design Read 的五项上下文和五项视觉观察。
- `artifacts` 的六项必需材料：`final_render/thumbnail/reference_comparison/typography_proof/reference_blueprint/poster_plan`，每项给 `path/sha256`；`poster_plan` 必须指向当前渲染输出的 `poster_plan_review.json`，不沿用修改前输入。相对路径以 review 文件所在目录为基准；需要中英双版时加 companion PNG/SVG 等证据，并分别对各语言终图审批。
- `preflight` 和 `anti_default` 的逐项判断及证据；所有疑点需消除或有语境依据。
- `design_scores/production_scores`：每个分项填 `score/evidence/artifact_refs`，引用本 review 中存在并校验过的材料名。不能自行填写另一个总分覆盖计算结果。
- `issues`：没有发现问题时为空列表；修复过的问题保留闭环记录。

[poster_review.py](../scripts/poster_review.py) 从 [唯一评分配置](../core/design_quality_scores.yaml) 读取每项满分和 82/85 门槛，拒绝缺项、负分、超满分、布尔值和非有限数；检查材料哈希、必需检查、语境例外与未闭环问题。旧五段观察式 review **不再允许正式交付**，须按新模板补齐并重新看图。78 分旧 critic 已取消独立评分；早期路线筛选分数不是最终验收门槛。

文件哈希与结构通过只说明证据可追溯；代码不能验证评审者确实看图，也不能自动判定审美、事实来源或理由真实。必须由有看图能力的评审负责判断；合成测试数据不能充当生产评审。

## 3. 最终像素可读性硬门禁（独立于 15 分评分）

生产用 `Poster Plan → SVG → 最终 PNG`，同渲染器另得无文字底图与各文字掩膜，逐块测局部像素。**不能只看 CSS 的文字颜色、整体平均亮度或字体已加载。**

默认核心指标（具体代码与模块 README 为准）：

- 普通文字局部对比 ≥ **4.5:1**，大字 ≥ **3:1**；文字核心像素达标比例 ≥ **92%**，第 10 百分位不得低于阈值；
- 检查局部纹理、亮度变化、真实主体保护区 `protected_regions`、25% 缩略图的 H0 和关键信息大小/亮度信号；
- 低对比、遮住已标记的关键主体、关键文字缩略不可辨识 → 技术 FAIL；复杂背景即使对比合格，仍需视觉复核；
- 只能做风格授权的局部位置移动、approved 色板改色、限额 `local_tint`；最多 **2** 轮真正重渲染/复测，不能用全页黑蒙层、粗描边强行过关；
- 无 `protected_regions` 时，不得声称“已自动避开人物/展品”；当前系统不自动理解所有图像语义。

```bash
python layout_engine/readability/audit_and_repair.py poster_plan.json --out-dir build/readability
```

输出 `readability_report.json`、`final_render.png`、`poster_final_review.svg` 等可追溯材料。**只生成 SVG/PNG 是 DRAFT**，即使 `technical_readability_gate=PASS`，`final_delivery_allowed` 仍为 false，直到具备看图能力的评审实际查看最终图，提交绑定**当前最终 PNG SHA256**的视觉审查 JSON 并重新运行 `--visual-review`。

```bash
python layout_engine/readability/audit_and_repair.py poster_plan.json --out-dir build/readability --visual-review build/readability/review.json
```

真实视觉复核执行上述完整协议；最终 PNG 与缩略图 SHA、材料哈希或问题复验不匹配时拒绝通过。`review_issues` 列出拒绝原因，分项总分由代码计算。不能通过重新填写分数替代图像复核。带 `--visual-review` 而验收未通过时，CLI 退出码为 4；像素技术失败为 3，不带 review 的技术预检仍不代表正式交付。

## 4. 交付与限制

交付中文/英文两套事实一致的 SVG + Poster Plan + 导出预览/终图及报告。SVG 可包含嵌入位图，**不表示所有图形都矢量化**；Figma 导入后是否保留原生文本对象不作保证。CairoSVG/Pillow 的可读性测量与浏览器/印刷端可能不同，差异需目标端复验；工具无法验明 AI 直接写进位图的正式文字是否正确。

历史测试审计是证据记录，不可等同于本次项目已完成真实生图或审美保证。
