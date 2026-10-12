# Reference Library Coverage v0.13

本轮导入 `海报风格参考.zip`，共索引 **113 张静态海报参考**。另有 1 个 mp4，本版不作为视觉 anchor 使用。

## 初始视觉簇
这些是“检索簇”，不是已经成熟的 Style Pack。初始分组会在后续用视觉分析继续修正。

| Cluster | 数量 | 当前用途 |
|---|---:|---|
| R01_PLAYFUL_HANDDRAWN | 14 | 年轻手绘 / 社群 / 市集 / 涂鸦 |
| R02_MINIMAL_EDITORIAL | 13 | 极简编辑 / 机构 / 安静文化活动 |
| R03_EXPERIMENTAL_TYPOGRAPHIC | 29 | 实验排版 / 字体 / 艺术展 / 瑞士解构 |
| R04_ACID_DIGITAL_EXPERIMENTAL | 16 | 酸性 / 荧光 / 数字视觉 / 新媒体 |
| R05_DIFFUSE_GRADIENT_ABSTRACT | 4 | 弥散 / 渐变 / 柔光抽象 |
| R06_SOFT_NARRATIVE_ILLUSTRATION | 7 | 轻量叙事插画 / 生活场景 |
| R07_BOLD_EVENT_POP | 2 | 音乐 / 大色块 / 强活动感 |
| R08_PHOTO_CINEMATIC | 1 | 摄影 / 电影 / 情绪型 |
| R09_COLLAGE_ZINE_MIXED | 12 | 拼贴 / zine / 独立出版 / 混合媒介 |
| R10_LIFESTYLE_CULTURAL_EDITORIAL | 15 | 生活方式 / 阿那亚 / 天目里 / 公共文化活动 |

## 覆盖判断
### Coverage A — 可直接用于强检索
参考 >= 10 且视觉语法相对丰富：R01/R02/R03/R04/R09/R10。

### Coverage B — 可做辅助 anchor，不宜单独定义成熟风格
参考 5–9：R06。

### Coverage C — 明显不足
参考 < 5：R05/R07/R08。

当任务落在 Coverage C 时，不允许假装“风格库已经覆盖”。必须触发 Coverage Gap Policy。

## 非覆盖类型示例
当前参考仍可能不足：
- 高级商业摄影 / 奢侈文化活动
- 传统文化 / 非遗的现代转译
- 戏剧 / 舞蹈 / 古典音乐的高情绪舞台视觉
- 纯字体国际主义的系统化系列
- 复杂博物馆文物摄影
- 建筑 / 城市论坛 / 学术会议
- 纯 3D / CG / 建模类主视觉

因此 Library 的目标不是“包含所有类型”，而是：
1. 已覆盖时强检索；
2. 覆盖不足时诚实识别；
3. 优先寻找结构上最接近的 Lead Reference；没有 Lead 时再做 concept-led extrapolation，而不是把多个风格平均混合。
