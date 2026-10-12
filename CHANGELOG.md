# 更新记录

## 2026-10-13 · v0.19.1 参考库与增量维护
- 导入关键词批次 401 张，保留原 113 个编号和路径；统一索引 514 条记录对应 401 张不同图片，哈希别名用于去重。
- 新增批次 manifest、四维 facets、未知项队列、分页接触表和离线图库。
- 新增幂等导入、编号冲突拒绝、图片哈希/尺寸校验、关键词候选检索及七项回归测试。
- 保留主分支已合并的六份主题文档结构，同步技能入口与参考系统机制；原图标签仍待视觉确认。


## 2026-10-12 · v0.19 文档去重与规则一致性整理（不改变引擎版本）
- 将约 26 份根目录规则说明整合为 `docs/` 下 6 份主题规范；删去冗余入口文档，旧内容可从 Git 历史恢复。
- `SKILL.md` 改为简短唯一任务协议；`ACTIVE_RULE_INDEX.md` 明确代码、YAML、规范、历史审计的优先级；README 更正 `core/` 为 46 个 YAML。
- 统一解释粗筛/精拆阶段权重与 `core/reference_deconstruction.yaml` 的 92 点子项权重，消除旧版 75 点子项说明造成的冲突。
- 将三种 H0 设计策略映射到 SVG 执行器支持的 `STANDARD_BLOCK/CUSTOM_GLYPH`；不修改执行器参数接口。
- 将 v0.12–v0.17 的过期审计文档移至 `audit/history/`，保留历史证据。
- 本次为**文档/结构整理**，不宣称新增视觉生成能力或重新通过所有运行测试。

## v0.19 · 最终叠字画面可读性（2026-10）
增加 `layout_engine_v018/readability/audit_and_repair.py`：SVG 真实渲染、无字底图与文字掩膜对照、局部对比/复杂度/主体标注、受限修复、重新渲染、以最终 PNG SHA256 绑定的视觉复核。原 SVG 导出仅 DRAFT。

## v0.18 · SVG-first 双语排版
以 SVG + JSON Poster Plan 为权威排版源文件；默认标题 `STANDARD_BLOCK`，仅有可核验矢量字形证据时用 `CUSTOM_GLYPH`。HTML 可选作预览，不再是唯一母版。

## v0.17 · 多路线编译器与用户否定优先
原 v0.16 同一参考下伪 A/B/C 路线被修正为真正不同的 Lead / Palette / H0 / Concept 组合；用户否定覆盖旧 Design 自评分，Prompt Compiler 不负责直接调用生图模型。

## v0.16 · 初版 Prompt Compiler
引入结构化路由输入与提示词编译；后续在 v0.17 修正对单路线和演示样例的过度依赖。

## v0.15 · 中文字体技术与视觉双重门禁
真实字体文件与字形覆盖、TTC face、字形样张、浏览器证据、专属展示字条件和字体下载授权。

## v0.14 · Brief 断点与可选模型适配
新增事实预检、LoRA 后端能力与许可/下载门禁，无可用适配器时 BASELINE_ONLY。

## v0.13 · 参考图忠实度与艺术字策略
引入 Lead/Support、Reference Blueprint、Structure/Surface/Typography Delta 及 H0 按参考选择设计模式。更早版本留存于 Git 历史。
