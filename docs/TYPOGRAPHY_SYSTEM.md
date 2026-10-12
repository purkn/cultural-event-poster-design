# 中英字体、H0 艺术字与技术证据规范（v0.19）

> 合并原 `TYPOGRAPHY_ENGINE_V015`、`TYPE_SPECIMEN_SOP`、`FONT_DOWNLOAD_BREAKPOINT`、`TYPOGRAPHY_REFERENCE_GATE`、`TYPOGRAPHY_STRATEGY_ROUTER`、`H0_REFERENCE_FIDELITY_GATE` 与 H0 实现限制。中文/英文分别验收。

## 1. 先选择设计策略，再映射到技术执行模式

**设计策略**（`core/h0_strategy_router.yaml`、`core/h0_design_gate.yaml`）与 **SVG 参数**（`layout_engine_v018/schemas/poster_plan.schema.json`）是两个层级，不能直接混用：

| H0 设计策略 | 条件 | SVG 实现模式 |
| --- | --- | --- |
| `REFERENCE_LED_DISPLAY_TYPE` | 参考中真实字库与精确排印已构成设计 | `STANDARD_BLOCK`（真实 SVG 文本） |
| `GLYPH_SAFE_ARTWORD` | 参考确实要求定制笔画/手写结构 | 完整真实字形可用 `STANDARD_BLOCK`；需要逐字形变时只有带可信路径和证据的 `CUSTOM_GLYPH` |
| `IMAGE_INTEGRATED_H0` | 参考的图像与字形在构图中嵌合 | 无字形改造时 `STANDARD_BLOCK` 配合图层；实际定制轮廓须用 `CUSTOM_GLYPH` |

`CUSTOM_DISPLAY` 是特殊的字体制作分支/描述，不是 `h0.mode` 的合法值。**当前执行器只有 `STANDARD_BLOCK` 和 `CUSTOM_GLYPH` 两种模式**，不可填写另三种设计策略当作 `mode`。H0 采用不同大小/旋转的单字符 CSS 拼装作为默认艺术字，一律拒绝。

## 2. 字体人格分析

参考 H0 至少拆：骨架 serif/sans/brush/custom、笔画反差、字重、宽度、垂直比例、端点、组合方向、填充、纹理/特效、与主视觉相交的方式。正文、英文、数字还须记录字系性格、字重阶梯、大小写、字距、数字形态和 label/value 层级。

Lead 如果是专属展示字，不能只用“宋体/黑体”代替，必须拆到笔画与字面关系；无法从图片证明实际字体名称时标记 unknown。字体可以选择成熟真实字库+结构化排版，不以“没有渐变”判为失败；只把效果堆在普通字体上，也不能因此判成艺术字。

## 3. H0 的技术与视觉双重门禁

- **技术 `TYPE_GATE_TECH`**：获得本地合法字体文件路径、hash、family/style、TTC face index、实际简繁地区字形；用 fontTools `cmap` 证明字符覆盖；不得隐式合成字重、混用 fallback。文字内容逐字核对，中文与英文分别运行。
- **视觉 `TYPE_GATE_VISUAL`**：将真实 Lead 标题裁片、至少 2 套（通常 3 套）候选字体样张、最终海报缩略图并排，逐项比较笔画、宽度、字距、形心、字图关系。自带有字库 ≠ 有美感；字符正确 ≠ 设计忠实。
- 使用浏览器时需要实际 `@font-face` 加载证据、字体与图像加载后截图；`getComputedStyle` 或 `document.fonts.check()` 单独不足证明没有 fallback。SVG 渲染器与目标端有差异时，继续在目标端核查。
- 无真实字体/字形样张/视觉证据时按 [质量规范](QUALITY_AND_DELIVERY.md) 的封顶/阻断处理，不能自评 85 分以上。

### 字体验证命令

```bash
python scripts/font_coverage.py --font /path/to/licensed-font.otf --text '壁上万象' --face 0 --out build/coverage.json
python scripts/render_type_specimen.py --font /path/to/licensed-font.otf --text '壁上万象' --face 0 --out build/h0-proof.png
```

**竖排中文**：区分编辑排印与浏览器段落竖排；逐字处理重心、端点、标点方向；英文/数字独立检查。

## 4. 字体下载与定制字断点

本地无可用且符合参考字形人格的字体时触发 `BP_FONT_DOWNLOAD`，主动推荐一款具名正规字体及可选本地替代，并说明作者/发行方、链接、许可证、文件大小（若可查）、费用、用途、嵌入/再分发限制、缓存位置。**用户明确授权前不得下载。** 拒绝可选择经验证的次优字体且标明视觉差异，或进入 `TYPOGRAPHY_UNRESOLVED`。

对于高定制 H0：从正确合法的真实字形骨架生成可核对的 SVG 轮廓，保存源文字、字符映射、矢量形变与证据；AI 位图中的伪文字不能作为正式活动信息。第三方字体二进制不得未经许可打包进入公开仓库。

**执行器边界**：SVG 源码中 `<text>` 可修改；导入 Figma 后是否仍为可编辑文字，取决于导入方式，不做保证。详见 [SVG 排版说明](../layout_engine_v018/SVG_FIRST_LAYOUT.md)。
