# Prompt Compiler v0.17 — 多路线编译协议

**绝不把示例当默认输入**。编译前从本次任务的 Brief 和素材构建 `schema_version=0.17` 的生产 JSON，路径不得位于 examples/golden/sample/test。用户已否定的路线要载入 feedback。所有步骤首先调用 `compile_routes_v017.py`，它只负责规范与 Prompt 生成，不负责视觉观察或真正生图。

## 路线单位而非 A/B/C 同色微调
一个 route 是 `{lead, color, typography, concept, layout}` 的整体。一轮至少两条真实不同的路线，且至少改变其中两个维度（失败重做时需要精确响应 user.must_change）。允许路线跨 Style Pack；缺 Lead 或理由不足时返回 STOP，不强迫套用 S01。

每条路线需有：
- `lead` 的真实图片路径、观察声明、四类 DNA（structure/medium/value/palette/typography）；
- `visual_idea`：主体是什么、发生什么动作、怎么影响空间组织，不能只写“一个罐子”；
- `palette`: background/dominant/secondary（可 `none`）、origin 与 palette_family；
- `typography`: H0 strategy、字体类别/具体身份或待设计路径，不能只有“playful”；
- `composition`: 画布比例、hero 区、H0 区、信息保留区；
- `negative`: 仅写与本次失败相关的明确禁止形态；
- `assets`: 有什么需要保留 / 可以改。

## 自动停机
- 真实内容缺失；候选 Lead 并未看过；文件路径不存在；候选路线重复；用户明确要更换的维度没换；字形路线复用被否定字体；当前用户不喜欢的 palette family 再次出现；与 Lead 的色彩/媒介明显冲突；没有足够路线来比较 → STOP（可补候选，不自动生成）。
- `supports_reference_images=false` 只是一种后端能力降级，非停机；必须输出 `TEXT_ONLY_REFERENCE_FALLBACK`，不能声称参考已送入模型。
- `supports_external_lora=false` → `BASELINE_ONLY`；兼容+授权后才进入原 v0.14+ LoRA 分支。该模块不下载任何权重。

## 编译输出
每条路线输出一份包含六大块的**具体主视觉提示词**：
1. lead 世界及何为借鉴，明确参考图并非“生成同一个对象”；
2. 主题与核心可见视觉动作；
3. 画面区域、焦点、层次与留白；
4. 色彩角色、表面媒介、图形密度；
5. H0 未来的准确字形占位与活动信息区；
6. 禁止的可见失败形态；后端可用时输出独立 negative channel。

每条路线打包 `reference_attachment`, `prompt`, `negative_prompt`, `capabilities`, `status=COMPILED_NOT_RENDERED`。执行后端真正把参考图作为输入才可标 `IMAGE_CONDITIONED`。

## 设计进度状态
生产输出：`NEED_NEW_ROUTE` → `COMPILED_NOT_RENDERED` → `RENDERED_NOT_REVIEWED` → `REVIEWED_PASS|REVIEWED_FAIL`，禁止直接 `COMPILED→DESIGN_PASS`。
