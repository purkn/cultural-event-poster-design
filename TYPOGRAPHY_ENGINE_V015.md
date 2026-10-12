# 中文字体质量引擎 / Chinese Type Assurance v0.15

> 优先修复中文排印设计能力及字体可复现性；规则适用于全部 Style Pack，不仅敦煌案例。

## 0. 本次诊断（不得把风格偏差误判为字符编码错误）
- FAIL：原 Lead `REF-097` 的「無常形」是具有高度定制化结构的展示字，而执行日志仅用“轻宋体/高对比宋体”描述，丢失字形结构与内在笔画关系。
- FAIL：生成的「壁上万象」四字可辨认，但大小感、字面宽度、字距和重心无法匹配 Lead，局部像系统字体随意竖排。
- UNKNOWN：缺实际 HTML/CSS、font files、浏览器 font logs，**无法断言**当次必然发生字体回退；必须通过新 Font Preflight 检证，不得只凭截图声称回退。
- FAIL：曾以“宋体真实字形+无渐变”代替 Typography Quality；这是技术属性而非审美证明。
- FAIL：仅因为视觉媒介 / 明度接近就给 Lead 4/4，忽略标题形态为品牌定制字，不能直接映射到任意 Songti。

## 1. 字体选择前必须完成 Type DNA 深拆
`type_blueprint.json` 包含：
- lead_id, reference_crop, locale, title_exact, title_script_variant(SC/TC), type_mode
- skeleton_class (Ming/Song/Grotesk/Brush/custom_display/mixed)
- construction (stroke endings, beam/curve/serif forms, stroke joins, counters, special ligatures)
- stroke_contrast, apparent_weight, apparent_width, cap-like xheight rhythm, vertical/horizontal center of mass
- per_glyph observations (不同字必须分别记，不能平均)
- composition (column count, orientation, glyph sizes, spacing, bounding boxes, scale against hero)
- surface (flat/texture/outline/gradient), measured fill role, reference evidence and uncertainty
- candidate_font_paths, candidate_license, glyph coverage report, font loading evidence
- reference_mismatch_risks

如果 Lead 的 H0 是 custom_display，必须标记 `reference_font_is_custom=true`；**不得直接归类成某款现成轻宋并宣称忠实模仿**。
不得从截图凭空猜测确切字体名称；字体识别未知写 unknown。

## 2. 中文 / 英文的字体优先级（针对每个语言独立证明）
A. 官方可用的活动品牌字形与正规授权素材；
B. 有许可证、已经安装且**逐字覆盖并经样张对比合格**的本地字体；
C. 推荐可合法下载字体，触发 `BP_FONT_DOWNLOAD`，明确来源、授权、体积和应用范围；
D. 若无合适真实字形，则从真实汉字骨架生成可校对的定制矢量艺术字，保留原始文本语义层及逐字核对证据；
E. 仍无法满足 → `TYPOGRAPHY_UNRESOLVED`。不允许用浏览器自动 fallback、“系统宋体”或高分自评掩盖。

必须区别：文字正确 ≠ 字体文件正确 ≠ 字形设计正确。

## 3. 强制字体技术预检
1. 获取**真实本地字体文件路径**，记录文件 hash、family/style/字重、face index（TTC/OTC 字体集合），并检查区域字形（SC/TC/JP/KR）；同一字符 Unicode 覆盖不意味着所选 face 的汉字结构适配。
2. `fonttools` 静态检查所需中文、标点、英文、数字是否全部有 glyph cmap 映射；必须覆盖本次所有 H0 字符（空白除外）。
3. 检查相同 H0 内字符是否来自混用字体；禁止标题中悄然混合多个后备字体。
4. CSS 对每个角色使用 `@font-face` 加载**显式资产路径**；`font-display:block` 可用于截图库，必须等 `document.fonts.ready` 和图像解码完成才截图。
5. 禁止 `font-synthesis` 偷偷合成粗体、斜体（`font-synthesis:none`）；不准用 CSS `scaleX()` 拉细宋体当真实 condensed 设计。
6. 必须附 Font Probe 结果 + 浏览器 font-face evidence + 角色样张。`getComputedStyle`/`document.fonts.check` **单独不足**证明无回退。

工具：`scripts/font_coverage.py`；`scripts/render_type_specimen.py`；`scripts/type_browser_audit.py`。

## 4. 字体设计的两阶段门禁
### 4.1 TYPE_GATE_TECH（机械）
全字覆盖、许可证确认、font face 可加载、没有合成字重、文本字符完全一致、无缺字豆腐框 / 截断、实际页面无不期望的字形回退。失败即 BLOCK_RENDER。
### 4.2 TYPE_GATE_VISUAL（审美）
将参考标题裁切、候选标题等比例单独呈现（同背景/明度比较），以及实际完整海报缩略图并排：
- 结构人格是否相同？如定制图形字 vs 现成宋体，不相同即 RED。
- 笔画粗细对比、端点、字面宽度、四字节奏、组合后的轮廓是否匹配？
- 标题与画面主视觉的压缩/穿插关系是否匹配？
- 中文版独立成立吗？是否可辨认且没有低质转换？
- 标题是否过于像“廉价网页竖排”而非文化海报？
**Type Visual RED 不得用文本准确率、无渐变、无碰撞或 production score 抵消。**

## 5. 竖排中文专项
- 最优先先决定“设计上是纵向组合的字”还是“浏览器标准竖排段落”。不要默认 `writing-mode:vertical-rl` 就完成设计。
- 展示型 H0 采用逐字可控组时：每字的字面、对齐、重心、行进方向、空隙都需自定义；先保证阅读顺序自然。
- 正文纵排如用 writing-mode，独立处理拉丁字符的 `text-orientation` 与标点，避免数字错旋转；不能把英文横排规则直接翻译到中文版。
- 提供 title-safe bounds，标题任何字不得碰撞信息区，也不能靠视觉越界冒充设计。

## 6. 按字体模式分流（跨风格）
- `REFERENCE_LED_DISPLAY_TYPE`: 可使用优秀真实字体但必须有“候选样张比较”；如果 Lead 是 custom_display，必须转为 custom glyph route 而非强行普通字体。
- `GLYPH_SAFE_ARTWORD`: 真实文本 → glyph outline → 人工/受控形变 → 矢量层 → 逐字校对；不能让自由生图决定汉字。
- `IMAGE_INTEGRATED_H0`: 在保持字符骨架可读的前提下跨图字融合；输出保存对应 HTML 文本层以确保信息可访问。
- `CUSTOM_DISPLAY`: 有 Lead 明显独特字形时的显式新路由。借用设计原则，不直接复刻另一品牌的独特字形或专属 logo。

## 7. 如果没有合适字体
`BP_FONT_DOWNLOAD` 推荐具体开源/授权字体 + 明确许可路径、下载大小、字体角色和预计使用范围，请求同意后才下载。拒绝后重新筛本地字体并给出诚实的匹配评分；不准改口说任意系统字体“同频”。不得在 ZIP 打包/再分发非授权字体文件。

## 8. 证据等级与评分封顶
- 未完成字体文件预检：Production 不得 PASS；H0 Design 项封顶 25%。
- 无候选字形样张 / reference crop 并排证据：Typography Design 项封顶 40%。
- 对 custom-display Lead 用普通系统 Songti 代替且未做字体再设计：Type Visual RED。
- 未检查中英两版：双语 typography 不得 PASS。
- 自评 85+ 而无 font provenance / Type Delta 证据：`EVIDENCE_FAILURE`。
