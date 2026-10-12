# v0.13 敦煌生成稿 — 中文标题排印失败分析

## 观测资料
- 输入：本包 `case_studies/V13_DUNHUANG_CJK_FAILURE/generated_zh.png` 和 `lead_REF-097.jpg`。
- 可确认的是字形设计问题，不是从图像就能确认“浏览器 fallback”或 Unicode 文件损坏。
- Lead 原图经平台转载，外围含黑边与下方账号信息，分析时应裁切到海报本体，而非学习水印/黑边。

## Lead 实际 H0 视觉语言
不是简单“薄宋体”：有异乎常规的汉字笔画组合，字体极具定制性、字形自由变奏。标题周围有稳定的信息锚点，主文字的笔画和横向辅助英文、中文尺度对比鲜明。不能从一张 JPEG 断定它使用的字体名字。

## 生成图的问题
- 「壁上万象」以四个独立直立字列在右侧，较 Lead 的视觉排布机械；
- 每字宽度、视觉中心、书法骨架以及纵向间距缺统一设计，不等于“汉字乱码”；
- 白色纯色、没有渐变都做对了，但“有没有效果”不能代替字形与构成的评估；
- 大量完整展厅摄影 + 字置右侧，与 Lead 的高能流动液态型画面不是同一重心系统；
- 正确的自动流程应先尝试多款确有字体文件的候选，出标题样张；若想达到 Lead 的定制字感，必须走受控字形再设计，不准伪装为 Songti Light 解决。

## 诊断报告填空样例
- TECH: `UNVERIFIED`（缺那次 HTML/CSS、font path、渲染日志）
- VISUAL: `FAIL`
- Type strategy: `custom-display candidate required`
- Severity: `BLOCK_DESIGN_PASS`
- Recommendation: compare 3 actual face candidates in proof, develop bespoke artwork only after their contours are evaluated.
