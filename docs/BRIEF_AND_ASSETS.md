# 活动简报、素材与断点规范（v0.19）

> **执行范围**：任何主视觉生成、LoRA 检索或字体下载之前。入口为 [scripts/preflight_brief.py](../scripts/preflight_brief.py)；以实际执行器支持的字段名为准。本文合并原 `BRIEF_INTAKE_BREAKPOINTS.md`，不另设平行规则。

## 1. 信息可信度与事实约束

每个活动字段记录 `{value, status, source, official}`，其中 `status` 为 `confirmed/draft/missing`，`source` 可为 `user_pdf/user_text/user_asset/official_source/inference`。推测或示例内容不得标作 `confirmed`。中英文正式名称、日期、地点、票价、主办方和二维码落点不得虚构。

## 2. 缺口等级

| 等级 | 何时触发 | 处理 |
| --- | --- | --- |
| P0：阻断生产 | 正式活动名缺失；未获预热豁免的日期缺失；线下场地或线上访问方式缺失；用户指定必须呈现的票价、报名链接、正式主办方缺失 | `WAITING_FOR_USER`；一次集中询问真正缺少的独立信息，暂停正式生图和下载 |
| P1：定稿前确认 | 中英专有名称译法不确定、不同来源的日期场地冲突、二维码落点不明、版权/肖像/文物使用范围不清 | 可做标注草稿，不可擅自定稿 |
| P2：不阻断 | 缺 Logo、缺主视觉、未指定受众、未给原创 slogan、未指定尺寸 | 提供文字署名、合规 AI 主视觉或显式工作假设；默认可建议 4:5，但不可声称是用户要求 |

**预热豁免**：只有用户明确选择 teaser 且允许 TBA，才可将日期/地点标为待公布。线上/混合活动需要相应访问方式，不能只检查物理场馆。

**字段名准确性**：人类 Brief 可能称 `title`、`registration_link`；执行器的 JSON 使用 `fields.title_zh/title_en`、`fields.registration_url` 等结构。编写输入时以 [scripts/preflight_brief.py](../scripts/preflight_brief.py) 为准，不要把本段示意名称当作现有 JSON Schema。

## 3. 断点与授权

- `BP_CONTENT`：在生成前列出必要缺口，不为了可选 Logo 反复阻断。
- `BP_CONFLICT`：同时指出冲突来源，要求用户指定版本。
- `BP_ASSET_RIGHTS`：对来源、可改编范围、肖像/授权不清的素材请求说明；不伪造商标和版权。
- `BP_FONT_DOWNLOAD`：只有本地无适合且可合法使用的字体时，推荐具名选项，说明来源、许可、大小、费用、缓存与拒绝方案，用户明确同意后下载。详见 [字体规范](TYPOGRAPHY_SYSTEM.md)。
- `BP_LORA_DOWNLOAD`：必须先验证后端、底模及许可证，再请求某一个特定 LoRA 的当次授权；不同模型不可复用同一次同意。详见 [可选 LoRA](OPTIONAL_LORA.md)。

断点暂停当前操作；不得声称已在后台继续。关键状态以执行器为准：`WAITING_FOR_USER` / `READY_BASELINE`；无 LoRA 支持时 `BASELINE_ONLY` 不属于失败。

## 4. 素材处理与双语

对上传的照片/图形先记录保留、裁切、去背景、调色、矢量重建或不能修改等条件。正式中英文两版核对专名、时间和数字的一致性；官方英文名称不存在时先标草译。SVG 版式中以真实可校验的文字层写入活动事实。

**预检示例：**

```bash
python scripts/preflight_brief.py examples/brief_complete.json
```

该命令仅检查活动数据，不执行生图。
