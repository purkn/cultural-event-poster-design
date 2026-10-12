# 字体、H0 与艺术字规范（v0.19）

## 双层模式，避免概念冲突
设计策略不是排版引擎参数。视觉设计可选择：
- `REFERENCE_LED_DISPLAY_TYPE`：参考驱动的真实字体与精确排版；
- `GLYPH_SAFE_ARTWORD`：从正确真实字形出发的可校对定制展示字；
- `IMAGE_INTEGRATED_H0`：具备可读字形与图像互锁关系；
- `CUSTOM_DISPLAY`：Lead 明显是专属字形且现成字体不适配的特殊执行分支。
SVG 代码参数则为 `STANDARD_BLOCK`（真实文本块）或 `CUSTOM_GLYPH`（经核验的路径）；前三种创意策略并不一一对应 SVG 模式。必要时保留正式文案文本层，不能让位图 AI 伪字承担活动信息。

## 字体技术门禁
本次中文与英文分别记录准确标题、简繁体、来源、字体文件路径/哈希、family/face、字符覆盖及许可证；不得仅凭 CSS `font-family` 或 `document.fonts.check()` 声称无回退。不能合成不存在的字体字重、将 `scaleX` 当窄体、偷用系统宋体冒充参考。可使用 `scripts/font_coverage.py`、`scripts/render_type_specimen.py`、`scripts/type_browser_audit.py` 分别取证。

## 字形视觉验证
至少对比两套候选 H0 样张，按参考裁片观察笔画、字宽/字重、端点、排列节奏与图字关系；中文正确不等于字体人格正确。定制字不能静默退化为普通排印，也不应靠无依据渐变/描边/发光制造“艺术字”。原尺寸与缩略图都要真实看图。
采用纵向标题时，逐字重心、阅读顺序、拉丁数字与标点需独立设计；禁止无证据逐字随机旋转与缩放。代码层限制详见 `layout_engine_v018/H0_VARIATION_GUARD.md`。

## 缺字体时的断点
如果无已授权、全字覆盖且风格合适的本地字体，先提出具体推荐及本地退路，说明作者来源、许可、用途、下载大小与保存位置。用户未授权不得下载；未知来源/许可不得使用或打包转发。拒绝后可使用明确标注不足的合规备选或停在 `TYPOGRAPHY_UNRESOLVED`。

## 交付门禁
真实字体加载、字形技术审计与视觉审计分别判定，不得用 Production 分数覆盖字形不匹配。中文、英文分别验收；详情由 `QA_ACCEPTANCE.md`、`core/chinese_typography_gate.yaml` 和实际代码控制。
