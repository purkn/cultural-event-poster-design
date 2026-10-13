# 有效规则索引 v0.20.0（唯一冲突裁决入口）

## 权威优先级

1. `SKILL.md`：**唯一**任务生命周期、阶段和断点协议；必须先满足活动事实与版权边界。
2. **运行时真实代码 / Schema**：`scripts/preflight_brief.py`、`scripts/poster_review.py`、`scripts/compile_routes.py`、`layout_engine/scripts/build_poster_svg.py`、`layout_engine/readability/audit_and_repair.py`、`layout_engine/schemas/poster_plan.schema.json`；命令、字段和值以这些实现为准，不得从旧文档推断未实现能力。
3. **定量配置**：`core/*.yaml`（评分与 Reference 等参数）；最终分项满分和门槛只定义于 `core/design_quality_scores.yaml`，评审清单只定义于 `core/universal_poster_critic.yaml`；若与旧文字规则冲突，代码可运行的字段优先；文档需改为如实描述，不随意修改硬门禁。
4. **五份主题文档**：`docs/BRIEF_AND_ASSETS.md`、`docs/REFERENCE_SYSTEM.md`、`docs/DESIGN_AND_ROUTES.md`、`docs/TYPOGRAPHY_SYSTEM.md`、`docs/QUALITY_AND_DELIVERY.md`；与代码并存时负责解释**原因及操作过程**，不另设重复阈值。
5. **模块说明**：`modules/prompt_compiler/PROMPT_COMPILER.md`、`layout_engine/README.md`、`layout_engine/readability/README.md`，负责对应模块的操作细节；不得推翻上级硬门禁。
6. 历史 changelog 与 Git 提交 仅为过去版本的证据，**不是有效运行规范**。

参考库运行机制以 `scripts/reference_library.py` 与 `reference_library/README.md` 为准；统一索引按批次 manifest 重建，保留历史别名，关键词只用于粗检索，不覆盖视觉 Lead 门禁。

## 防误用：三个容易混淆的层级

- **参考权重**：粗/精检索阶段的 25/75 说明不能替代精拆子项权重；目前 `core/reference_deconstruction.yaml` 的 `rerank_weights` 总和 **92**。需要比例时按 92 归一化。详见 [参考规范](docs/REFERENCE_SYSTEM.md)。
- **H0 策略与执行**：三个视觉设计策略经映射后仅使用 `STANDARD_BLOCK` 或 `CUSTOM_GLYPH` 两种 SVG 合法模式。详见 [字体规范](docs/TYPOGRAPHY_SYSTEM.md)。
- **结构预览与可交付稿**：SVG 生成脚本完成的是 DRAFT。最终 PNG 像素检查、真实视觉审查和当前 SHA256 绑定均完成后，才可能 `final_delivery_allowed=true`。Design ≥82、Production ≥85 不能替代单独硬门禁。

## 止损与回退

Brief P0 不全 → WAITING_FOR_USER；Lead 不合适/用户否定路线 → NEED_NEW_ROUTE；字体未授权或不匹配 → TYPOGRAPHY_UNRESOLVED；最终技术可读性失败 → 回到布局或素材设计；未查看实际图或无绑定 SHA256 的复核 → VISUAL_REVIEW_PENDING，不得声称正式 PASS。
