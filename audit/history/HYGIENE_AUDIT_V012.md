# v0.12 Skill Hygiene & Shortcut Audit

## 结论
v0.12 当前包在**文件卫生、数据可解析性、规则优先级、反偷懒路径**四方面通过本轮检查。

## 1. 文件卫生
扫描结果：
- 总文件：252
- Markdown：40
- YAML：54
- JSON：16
- CSV：1
- HTML：1
- PNG：6
- JPG：134

未发现：
- `.DS_Store` / 隐藏垃圾文件
- 临时 `.tmp/.bak/.swp` 文件
- 嵌套 zip/tar/7z
- 符号链接
- 可执行脚本
- YAML / JSON 解析错误
- 损坏 JPG / PNG
- 完全重复的规则文本文件

### 修复记录
本轮审计发现旧文件 `core/theme_specificity_gate.yaml` 有一个 YAML 未完整引用的字符串，已修复并重新验证全部 54 个 YAML 可解析。
上一版 audit 已移入 `archive/audits/`，避免被误当成运行时规则。

## 2. 规则卫生
新增 `ACTIVE_RULE_INDEX.md v0.12` 作为权威顺序。
当前运行时主规则统一为 v0.12；历史诊断与旧审计仅存在于 `archive/`。

检查未发现：
- Design 78 与 Design 80 两套并行门槛
- 2 rough / 3 rough 的 LOW coverage 冲突
- Reference Quartet 与 Lead First 的并行默认规则

当前统一门槛：
- DESIGN >= 80
- PRODUCTION >= 85
- LOW coverage rough >= 3
- Lead Reference First + max 1 Support

## 3. 本轮重点发现的偷懒路径

### A. Reference-to-keywords Shortcut — 已封堵
旧症状：
“参考图 = 手绘 + 大字 + 留白 + 不对称”。

修复：
- `REFERENCE_DECONSTRUCTION_ENGINE.md`
- `REFERENCE_BLUEPRINT_CONTRACT.md`
- `core/reference_deconstruction.yaml`

有 Lead 时，没有结构 Blueprint 不允许进入 Rough。

### B. False Reference Match Claim — 已封堵
旧症状：
成稿与 Lead 结构明显不同，仍声称“拓扑高度一致”。

修复：
- `REFERENCE_DELTA_GATE.md`
- 至少 8 个变量对比表
- RED Delta 不得 PASS

### C. Semantic Color Shortcut — 已封堵
旧症状：
草坪自动绿色、户外自动橙太阳蓝云、儿童自动彩虹。

修复：
- `PALETTE_STRUCTURE_GATE.md`
- 色彩按“角色+面积+明度/饱和度”评估
- 新增无证据高饱和色直接 Fail 规则

### D. Semantic Decoration Shortcut — 已封堵
旧症状：
户外补太阳云朵、音乐补音符、儿童补星星笑脸。

修复：
- `SEMANTIC_DECORATION_BAN.md`
- 无 Lead / Concept / Asset 证据的 filler 默认删除

### E. Fake Negative Space Shortcut — 已封堵
旧症状：
大片空白自动解释成“高级留白”。

修复：
- `NEGATIVE_SPACE_GATE.md`
- 必须有围合、方向、信息承载或尺度张力功能
- dead space 不计分

### F. H0-only Typography Shortcut — 已封堵
旧症状：
H0 做了艺术字，正文/英文随手用系统字体。

修复：
- `TYPOGRAPHY_REFERENCE_GATE.md`
- 正文、英文、数字、label/value 层级全部进入 Typography System

### G. Style Surface Shortcut — 继续封堵
旧症状：
只复制纸纹、蜡笔、颗粒，但结构不像参考。

修复：
- Reference Blueprint 优先于 surface style
- Delta Gate 中 H0、type-image relation、palette、negative-space 均为硬比较维度

## 4. V11 草坪音乐节已加入失败案例
`case_studies/V11_LAWN_MUSIC_FAILURE/`

它被用于回归测试以下问题：
- 配色语义化而不成熟
- 太阳/云等语义 filler
- H0 虽手写但专属性不足
- 声波概念没有真正控制结构
- dead space 误判为留白
- 与 Lead Reference 的真实结构关系过弱

## 5. 仍存在的真实风险
### Risk 1 — 参考库标签仍是 provisional
113 张参考图尚未逐张做完整结构 Blueprint。
这是有意采用 Lazy Deconstruction，而非错误：只有进入 Top 6–8 的候选才做精拆。

### Risk 2 — Reference Deconstruction 仍依赖视觉模型判断
目前 Blueprint 是规则约束，不是像素级自动测量器。
面积、密度、颜色比例允许估算误差，因此 Delta Gate 使用容差区间而不是要求精确数值。

### Risk 3 — 正式 Style Pack 仍只有 S01
参考库比 Style Pack 更丰富。遇到 S01 不适配的任务，应走 Reference Blueprint / Coverage Gap，而不是强行套 S01。

### Risk 4 — “强借鉴”仍有平均化风险
虽然已限制 1 Lead + 1 Support，但模型仍可能在语言上声称使用 Lead、视觉上自行发挥。
这正是 v0.12 新增 Delta Gate 的主要防线；后续测试应重点验证这一点。

## 6. 本轮审计结果
**PACKAGE_HYGIENE: PASS**
**RULE_PARSE: PASS**
**RULE_PRIORITY: PASS**
**SHORTCUT_RESISTANCE: PASS WITH REMAINING TEST RISK**
