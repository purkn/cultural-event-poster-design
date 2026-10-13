---
name: cultural-event-poster-system
metadata:
  version: "0.20.0"
description: 中文文化活动宣传海报设计工作流。活动信息预检、参考图主导的多方案生成、中文字体证据、双语 SVG 排版以及最终叠字画面可读性质检；真实生图依赖可用后端。
---

# 文化活动宣传海报 Skill · 唯一任务协议 v0.20.0

**职责**：根据活动简报、素材和视觉参考，执行创意路线、主视觉制作、中英文排版与质量审查。默认自主推进，**仅在真实事实缺口、授权/费用与不可替代的用户决策上设置断点**。不得把“需要审查”理解成每一步都询问。本文是流程入口；细节在 `docs/`，数值以相应代码/`core/*.yaml` 为准。

## 执行流水线

| 阶段 | 必须做什么 | 失败/断点 |
| --- | --- | --- |
| A. 简报与素材 | 执行 `scripts/preflight_brief.py`；核对活动名、日期、地点/线上链接、指定的票价/二维码/署名及来源。素材做权属和可修改性审计 | P0 → `WAITING_FOR_USER`；不编造事实、不生图 |
| B. 用户反馈 | 读取本项目适用的 `feedback_registry/`；明确必须避免的旧版路线指纹，不能把别的项目的否定全局化 | 用户已否定的方案 `USER_REJECTED`，旧自评作废 |
| C. 参考与概念 | 看真实参考图，粗筛、精拆并记录 Strong Lead / Support Scope；构建 Blueprint 和可见的 Concept 机制 | 无视觉证据不能宣布参考忠实；冲突需重新选 Lead |
| D. 路线与后端 | 至少两条真正不同的路线；检测后端是否支持参考图；运行 `scripts/compile_routes_v017.py` | 缺有效路线 → `NEED_NEW_ROUTE`；无法送参考图 → `TEXT_ONLY_REFERENCE_FALLBACK` |
| E. 主视觉 Rough | 调用实际可用的生图/素材编辑工具，分别生成候选并保存【Lead/Prompt/Rough】对照；先判断画面语言、配色、概念和用户反馈 | 无真实成图 → `NOT_VISUALLY_REVIEWED`，不能打 Design PASS |
| F. H0 与字体 | 按参考选择字体设计策略，检测真实字体授权/字形覆盖，制作至少两套字形样张；中文和英文分别比较 | 缺合法字体 → `BP_FONT_DOWNLOAD`；字体不匹配 → `TYPOGRAPHY_UNRESOLVED` |
| G. 排版与双语 | 使用同一份 Poster Plan 构建中文/英文 SVG，核对事实、字符、版式、安全区域；HTML 只能作为可选预览 | 越界、错字、伪中文字必须返工；SVG 仅为候选 |
| H. 最终可读性 | 必跑 `layout_engine_v018/readability/audit_and_repair.py`，对实际 PNG 与无字底图逐块测对比、纹理、缩略信息；仅做授权修复，最多两轮 | `technical_readability_gate=FAIL` 或 `must_escalate_layout` → 返回布局/主视觉 |
| I. 正式验收 | 真实视觉 Agent 检查最终 PNG、25% 缩略、主体遮挡及字体，并提交 **当前 PNG SHA256** 绑定的 review；分别验 Design 与 Production | Design <82 或 Production <85、硬门禁失败、无有效 `--visual-review` → **禁止交付 PASS** |

## 参考库粗检索（v0.20.0）

读取 [参考库维护说明](reference_library/README.md)。当前为 401 张不同图片；统一索引 401 条记录，113 个旧编号单独保存在 aliases.json。新批次 ID 为 `keyword-20261012:REF-XXX`，旧 ID 保留为别名，原图统一使用新批次路径，不能按同号替换。

运行 `scripts/reference_library.py query` 按活动、构图、字体、配色生成候选；检索按 SHA256 去重。文件名标签均为 provisional，16 张含未知标签；关键词得分不能作为 Strong Lead 证据。实际查看候选原图后按 `docs/REFERENCE_SYSTEM.md` 精拆与验收。增量导入、批次 manifest 重建、预览更新见库说明。

## 专题权威文档（按需求读取，避免全量重复加载）

- [活动信息、素材和授权断点](docs/BRIEF_AND_ASSETS.md)
- [参考图检索、Lead Blueprint 与 Delta](docs/REFERENCE_SYSTEM.md)
- [Concept、路线、反馈和防模板化](docs/DESIGN_AND_ROUTES.md)
- [H0 字体设计与真实字库证据](docs/TYPOGRAPHY_SYSTEM.md)
- [Design/Production 双轴及最终像素可读性](docs/QUALITY_AND_DELIVERY.md)

## 不可绕过的短路条件

1. **先事实后图**：P0 不齐不能以“先出效果图”伪装正式项目；可选 Logo 缺失通常不阻断。
2. **参考主导**：Lead 决定空间、明度、媒介、字体人格；Support 只能补一个明确局部缺口；有两项以上全局冲突应换 Lead。
3. **路由必须真实变化**：被否定的颜色/字体/视觉机制不能换个素材就继续；真实图片未看过，不许报告设计通过。
4. **字体策略 ≠ SVG 模式**：设计策略为 `REFERENCE_LED_DISPLAY_TYPE / GLYPH_SAFE_ARTWORD / IMAGE_INTEGRATED_H0`；执行器 `h0.mode` 只有 `STANDARD_BLOCK / CUSTOM_GLYPH`。无合法字形证据禁止逐字随机旋转缩放和 AI 伪字。
5. **技术≠审美**：Prompt 编译、字体加载、无水印、评分较高，不可替代实际 Rough 比图或最终视觉复核。
6. **叠字可读性阻断**：最终渲染局部低对比/关键主体遮挡/缩略不可辨识，不能拿其它分数补偿。无视觉 review 或 SHA256 不符时 `final_delivery_allowed=false`。

**版本冲突解决**：见 [ACTIVE_RULE_INDEX.md](ACTIVE_RULE_INDEX.md)。旧审计仅是历史证据，不能覆盖当前生产逻辑。当前可执行脚本不自动调用图像生成 API。
