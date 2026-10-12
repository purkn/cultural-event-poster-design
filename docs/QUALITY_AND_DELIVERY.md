# 质量验收、图文可读性和正式交付（v0.19）

> 本文合并原 `QA_ACCEPTANCE.md`、`DESIGN_QUALITY_CORE.md` 中评分和证据要求。**数值以 `core/design_quality_scores.yaml` 为权威；像素检测阈值以 `layout_engine_v018/readability/audit_and_repair.py` 为执行权威**，详细说明见 [readability 模块](../layout_engine_v018/readability/README.md)。

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

## 3. 最终像素可读性硬门禁（独立于 15 分评分）

生产用 `Poster Plan → SVG → 最终 PNG`，同渲染器另得无文字底图与各文字掩膜，逐块测局部像素。**不能只看 CSS 的文字颜色、整体平均亮度或字体已加载。**

默认核心指标（具体代码与模块 README 为准）：

- 普通文字局部对比 ≥ **4.5:1**，大字 ≥ **3:1**；文字核心像素达标比例 ≥ **92%**，第 10 百分位不得低于阈值；
- 检查局部纹理、亮度变化、真实主体保护区 `protected_regions`、25% 缩略图的 H0 和关键信息大小/亮度信号；
- 低对比、遮住已标记的关键主体、关键文字缩略不可辨识 → 技术 FAIL；复杂背景即使对比合格，仍需视觉复核；
- 只能做风格授权的局部位置移动、approved 色板改色、限额 `local_tint`；最多 **2** 轮真正重渲染/复测，不能用全页黑蒙层、粗描边强行过关；
- 无 `protected_regions` 时，不得声称“已自动避开人物/展品”；当前系统不自动理解所有图像语义。

```bash
python layout_engine_v018/readability/audit_and_repair.py poster_plan.json --out-dir build/readability
```

输出 `readability_report.json`、`final_render.png`、`poster_final_review.svg` 等可追溯材料。**只生成 SVG/PNG 是 DRAFT**，即使 `technical_readability_gate=PASS`，`final_delivery_allowed` 仍为 false，直到具备看图能力的评审实际查看最终图，提交绑定**当前最终 PNG SHA256**的视觉审查 JSON 并重新运行 `--visual-review`。

```bash
python layout_engine_v018/readability/audit_and_repair.py poster_plan.json --out-dir build/readability --visual-review build/readability/review.json
```

真实视觉复核至少覆盖主体遮挡、字体人格、层级、25% 缩略图与 Hero 完整性；SHA 不匹配视为旧证据，拒绝通过。不能通过重新填写分数替代图像复核。

## 4. 交付与限制

交付中文/英文两套事实一致的 SVG + Poster Plan + 导出预览/终图及报告。SVG 可包含嵌入位图，**不表示所有图形都矢量化**；Figma 导入后是否保留原生文本对象不作保证。CairoSVG/Pillow 的可读性测量与浏览器/印刷端可能不同，差异需目标端复验；工具无法验明 AI 直接写进位图的正式文字是否正确。

历史测试审计是证据记录，不可等同于本次项目已完成真实生图或审美保证。
