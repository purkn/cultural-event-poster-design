# 主视觉概念、路线选择与反套路规范（v0.19）

> 合并原 `DESIGN_QUALITY_CORE`、`EFFECT_DISCIPLINE_GATE`、`NEGATIVE_SPACE_GATE`、`SEMANTIC_DECORATION_BAN`、`PALETTE_AND_TYPE_DECISION_V017`、`ROUTE_RESELECTION_V017`、`VISUAL_QA_AND_SHORTCUT_AUDIT_V017` 的通用规则；量化评审见 [质量规范](QUALITY_AND_DELIVERY.md)。

## 1. 先确定可见概念，而非装饰关键词

每条路线需明确：活动的核心体验是什么、图中发生的具体视觉动作是什么、该动作如何改变主体比例、阅读路径、图字关系或空间结构。不得将“可爱、手绘、极简、动感”当作独立概念。核心原则是 **Concept → Reference World → Poster Craft**：概念可见、参考媒介可信、信息与视觉组合成熟。

可优先改变主体与图字的结构性关系，再选择细节效果。H0 可通过字体 DNA、位置、尺度、裁切、图字嵌合完成设计，不强制渐变/光晕/手写化。

## 2. 真实不同的路线与用户否定

新任务必须先读取本项目 `feedback_registry/`（如果存在对应任务的记录），并基于本次 Brief、素材、Lead 重新构造生产输入。负反馈**只在对应任务作用域生效**，例如某活动否定青蓝/旧纸/粗笨标题，不代表所有其它风格永久禁止这些元素。

至少准备 **两条真正不同**的路线，每条包含 Lead、色彩、H0 策略、Concept、布局与素材处理，原则上至少变化两个主要维度；编译入口为 [scripts/compile_routes_v017.py](../scripts/compile_routes_v017.py)，详见 [模块说明](../modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md)。

[core/route_competition.yaml](../core/route_competition.yaml) 还定义了探索期文本路线 6–10 条、常见 2 张 rough（低覆盖 ≥3）及特殊强参考例外。这是**更广义的创意探索/视觉候选评审规则**，与编译器“至少 2 条输入路由”不是同一数量层级；若真实执行该阶段，按对应配置记录，不可把仅两条编译结果冒称已经完成全部探索。

用户明确表示“丑、字体不喜欢、重复同样配色、不像参考”等：
- 立刻把当前方案标为 `USER_REJECTED`；旧自评分失效。
- 对比旧路线的 Lead、背景/主色家族、字体类别、视觉机制与 `route_fingerprint`，必须真正改变被否定的维度，不能只删几个星星或调整字距。
- 当前路线不能满足 `user.must_change` → `NEED_NEW_ROUTE`，重新检索；后端无法接收图像参考 → `TEXT_ONLY_REFERENCE_FALLBACK`，不得伪称已经发送 Lead。
- 先审视新 rough 的画面，再做水印、正文排版和高分评审。没有实际 Rough → `NOT_VISUALLY_REVIEWED`。

## 3. 色彩、装饰和效果的准入

每一色说明用途（背景、标题、Hero、强调、信息）、来源（Lead、素材、创意指导）和大致面积，不能把未测量的估算宣称精确百分比。

装饰仅在以下情况进入：参考中的对应语法、Concept 的结构职责、用户必保留资产、Style Pack Anchor Evidence。删除某个物件而 Concept、阅读顺序、构图均不变时，默认判定为 filler 并去除。禁止根据主题自动补太阳、云、音符、星星、杯子、叶子、网格等散点符号。大/中型装饰预算需与 Lead 的密度一致。

渐变、投影、描边、发光、3D、玻璃、金属、霓虹、纹理塞字等效果，必须提供 Lead/Style/Concept 的**结构证据**；不得靠装饰证明“有设计感”。有目的的留白需要产生围合、焦点导视、信息承载或尺度张力，不为“空”而空。

## 4. Rough 评审顺序

先做【Lead / Prompt / Rough】并排对照，判断：背景明度、色彩面积、媒介笔触与空间密度、H0 位置与字体人格、主题可见动作、用户否定的组合是否再次出现。缺实际图像或审图能力，不得发布 Design PASS。

`USER_REJECTED`、`DESIGN_FAIL`、`REFERENCE_DRIFT`、`TYPE_ROUTE_REJECTED` 必须回到路线或参考选择，不能靠后期润饰和 Production 得分覆盖。

生成模型调用、下载、参考图作为输入的实际支持情况必须按后端能力如实标注；Prompt Compiler **不负责自行调用生图模型**。
