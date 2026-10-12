# v0.13 Skill Hygiene & Shortcut Audit

## 1. 文件卫生
通过。

- 总文件数：269
- JSON：17，全部可解析
- YAML：58，全部可解析
- 图片：143，全部可读取
- 隐藏文件：0
- 符号链接：0
- 可执行文件：0
- 嵌套压缩包：0
- 临时 / 备份文件：0

## 2. 规则冲突审计
已修复的主要冲突：

### A. “H0 必须艺术字” vs “参考字体人格”
v0.12 的全局 Artword Hard Gate 会逼模型给任何 H0 加渐变、手写化或纹理。
v0.13 改为 Typography Strategy Router：
- REFERENCE_LED_DISPLAY_TYPE
- GLYPH_SAFE_ARTWORD
- IMAGE_INTEGRATED_H0

S01 手绘风仍默认 Artword；编辑/展览型参考可用真实字体骨架 + 定制排版。

### B. Lead First vs Support Override
v0.12 虽规定 Lead + 1 Support，但没有限制 Support 能改哪些维度。
v0.13 新增 Support Scope；Support 改动 2 个以上全局维度即 Hard Fail。

### C. Structure Fidelity vs Surface Drift
v0.12 主要比 topology，导致蓝白二维版画参考被生成成黑底多色发光分形。
v0.13 增加 Medium/Surface Fidelity，并把 high-key↔low-key、flat↔3D/generative 设为 RED。

### D. Reference Delta 过宽松
背景明度反转、H0 flat→gradient 等不能再作为 AMBER 自动解释。

### E. Style Pack 对所有风格强制 artword_grammar
v2.4 改为必须 `h0_strategy.yaml`；`artword_grammar.yaml` 只在相应风格需要时出现。

## 3. 发现并封堵的偷懒路径
1. **Topology-only Lead**：只因为“流动结构像”就选 Lead。
2. **Support Override**：用 Support 把 Lead 整体视觉世界改写。
3. **Artword-effect Shortcut**：为了证明 H0 有设计感，自动渐变/发光/描边。
4. **Immersive-glow Shortcut**：“沉浸/数字”自动黑底、多色、发光液体。
5. **Theme-color Shortcut**：“敦煌色彩”自动把多色渐变灌入标题。
6. **Production-score Inflation**：字准、无水印、无溢出不能抬高 Design 分。
7. **Reference-claim Shortcut**：只借到“流动”就声称高度参考。

## 4. v0.12 敦煌案例回归结论
Lead REF-105 与生成稿并排后，至少存在三项 Hard RED：
- high-key 蓝白 → low-key 黑底多色
- flat engraving/print → luminous generative/fractal
- light high-contrast flat H0 → heavy multi-color gradient H0

因此 v0.13 中该稿必须 FAIL，不允许再得到 Design 88。

## 5. 仍需后续验证的风险
- Reference Library 的 113 张图仍是 provisional cluster；新 Gate 能降低误用，但检索质量仍取决于索引质量。
- 当前正式成熟 Style Pack 仍主要是 S01；新增风格时必须按 v2.4 提供 h0_strategy + Surface Fingerprint。
- 真实字体文件/授权仍属于执行环境问题；Skill 只负责策略与断点，不能假定所有推荐字体已安装。

## 6. 结论
v0.13 当前文件卫生通过；未发现可执行或隐藏风险文件。主要“偷懒路径”已从规则层封堵，并新增 V12 敦煌失败案例作为回归测试。
