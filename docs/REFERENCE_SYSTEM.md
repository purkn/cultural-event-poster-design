# 参考检索、拆解和忠实度规范（v0.19）

> **唯一说明文档**。量化配置优先读取 [core/reference_deconstruction.yaml](../core/reference_deconstruction.yaml)、[core/lead_validity_gate.yaml](../core/lead_validity_gate.yaml)、[core/reference_blueprint_contract.yaml](../core/reference_blueprint_contract.yaml)、[core/reference_delta_gate.yaml](../core/reference_delta_gate.yaml) 与相关 `core/*.yaml`。本页整合原 Lead Validity / Dominance、Reference Deconstruction / Blueprint / Delta、Medium Surface、Palette Structure、Typography Reference 等重复说明。

## 1. 检索和角色分配

- 阶段 A：结合活动 Brief、媒介和构图特征，从 [参考库](../reference_library/README.md) 做粗检索。默认 `coarse_top_k=16`。
- 阶段 B：实际查看候选原图，拆解默认前 `deconstruct_top_k=8`，再排序。旧库 113 张图的 10 个 cluster 只是**临时检索标签**，不是十套已验证 Style Pack。
- **Strong Lead** 控制全局拓扑、媒介表面、背景明度、色彩角色、H0 字体人格、信息分区、留白和图字关系；不能只因为主题相似就选 Lead。
- **Support** 最多服务一个写明的局部缺口，必须记录 `support_scope`，不得用支持图覆盖 Lead 的整体视觉世界。
- 单纯结构相似、表面/字体/色彩不符的图片标记 `STRUCTURE_ONLY_REFERENCE`，只可辅助排版，不得冒充 Strong Lead。

### 批次索引与关键词粗检索（v0.19.1）

参考库现为 401 张不同图片，统一索引 514 条含 113 条旧编号别名。新增批次包含全部旧图，`aliases.json` 按 SHA256 映射旧编号到新批次编号，`image_path` 相对参考库根目录；旧图片路径保留。新增 ID 为 `<collection>:REF-XXX`，不能按序号匹配新旧作品。

`facets.json` 按活动 / 构图 / 字体 / 配色提供多维候选，不创建四份图片副本。运行：

```bash
python scripts/reference_library.py query --composition 非对称网格 --typography 无衬线 --top 16
```

关键词子串命中按构图 4、字体 3、配色 2、活动 1 排序，自动排除重复图片，返回实际命中字段。此分数只服务粗筛，不能套用视觉门槛。无命中时浏览旧簇与预览继续检索，不直接断言覆盖不足。

所有文件名标签均为 provisional；16 张含未知项。批次计数与标签覆盖见 `coverage.json`，待检查项见 `review_queue.json`；数量不代表媒介/H0/风格成熟度。批次 manifest 是元数据来源，导入与重新标注后使用脚本重建索引和预览，详见 [库维护说明](../reference_library/README.md)。

## 2. Strong Lead 判断

[core/lead_validity_gate.yaml](../core/lead_validity_gate.yaml) 的当前阈值：topology ≥0.70、medium/surface ≥0.65、typography DNA ≥0.60、palette/value ≥0.60、overall ≥0.68；原则上四维中至少三维达到中等匹配。阈值是项目内路由规则，并非客观测量海报美感的通用标准。

如果预计需同时打破两个以上全局维度（明度、媒介、H0 DNA、主轴、图字关系、色彩角色等），**重新选择 Lead**，不可生成完后才为风格漂移辩护。

## 3. Reference Blueprint 最小证据

必须记录三层：

| 层 | 字段 |
| --- | --- |
| Structure | H0/hero/信息 bbox、面积比、视觉中心、主轴、排版密度、最大留白区域及其功能、图字关系 |
| Surface | `medium_class`、2D/3D、背景明度类别、色彩角色及面积、笔触/边缘、光照模型、材质表面 |
| Type DNA | 标题骨架、笔画反差、字重/宽度、端点、组合方式、填充/效果、英文及数字配套字体逻辑 |

并写明 `BORROW`（继承的空间/媒介/字体语法）、`TRANSFORM`（主题、素材、文案转换）、`DO_NOT_COPY`（原作者独有角色、Logo、逐笔字形、像素级位置等）。默认容差以 [core/reference_blueprint_contract.yaml](../core/reference_blueprint_contract.yaml) 为准：H0/hero 面积比约 ±20%，视觉中心位移 ≤0.10 画幅，背景明度与媒介类别保持同类，色彩角色数差异不超过 1；有充分理由的 `PARTIAL_BREAK` 必须在生图前声明。

## 4. 权重统一（修复历史文档冲突）

**不要混用两个层级的比例：**
1. 旧人工规范提出“粗检索参考 25% / 精拆参考 75%”，指两个**阶段的组合影响**，不是精拆字段权重相加需要等于 75。
2. 当前 [core/reference_deconstruction.yaml](../core/reference_deconstruction.yaml) 的 `rerank_weights` 字段权重总和为 **92**（topology 15、medium_surface 14、H0_type_DNA 13、type_image_relation 10、palette_value_regime 10、density_negative_space 8、asset_structure 7、information_architecture 7、tone 4、event_semantics 2、format 2）。
3. 当需要转换成精拆内部百分比时，按 `100 × 当前项权重 / 92` **归一化**；不得把旧文档相加为 75 的另一套指标复制过来。这里描述的是评审计算口径，**不表示 Python 编译器已经自动实施视觉打分**。

## 5. Reference Delta 与禁止捷径

必须对照 Lead 保存 Structure、Surface、Typography 三类 Delta（GREEN/AMBER/RED）。以下为典型 **RED**：高明度↔低明度反转、二维印刷/版画→发光 3D、H0 字重跨两级以上、无依据的纯色标题→多色渐变/Glow、图字关系完全改变、Surface 或 Typography 两项以上显著冲突。

- 色彩先记录背景/主色/次色/点色的角色、面积、饱和度和来源；优先级 Lead → Style Pack → Concept → 主题联想。
- 不自动把“草坪=绿、传统=红金、科技=蓝紫霓虹”，不擅自增添不属于参考的透明玻璃、阴影或多色发光效果。
- 留白须承担围合、导视、适配信息或尺度张力中的至少两种作用；单纯大片空白不计质量分。
- 只有看过真实 Lead 和生成结果、保存并排证据，才能声称“忠实匹配参考”。文本 Prompt 编译不能代替实际生图评审。

关联：[字体规范](TYPOGRAPHY_SYSTEM.md) · [路线与反套路](DESIGN_AND_ROUTES.md) · [质量验收](QUALITY_AND_DELIVERY.md)。

数量按阶段区分：初始排序 shortlist 12 → 视觉候选扩展 16 → 深度拆解 8。拆解 rerank_weights 为相对权重（总和 92，排序时归一化），不是百分比。风格成熟度基准用 3–5 张，单路线批评从中选 2–4 张；二者不能互换。

Blueprint 的 H0 DNA 位于 `typography.H0_type_DNA`，项目必须填写 borrow、transform、do_not_copy 与 target_tolerance；schema 校验结构，真实借鉴质量仍由看图门禁判断。
