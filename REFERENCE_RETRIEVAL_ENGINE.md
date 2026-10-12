# Reference Retrieval Engine v0.13

## 目的
找的不只是“构图像”的图，而是能作为**完整视觉世界 Lead** 的图。

## Stage A — Coarse Retrieval
依据：
- visual topology need
- asset structure
- type-image relation
- information density
- H0 opportunity
- tone
- format
- event semantics
取 Top 12–20。

## Stage B — Fine Deconstruction
对 Top 6–8 拆：
- Structure
- Medium/Surface
- H0 Type DNA
- Palette/Value Regime
再重排。

## Fine Score
- topology 15
- medium_surface 14
- H0 Type DNA 13
- type-image relationship 10
- palette/value regime 10
- density/negative-space 8
- asset structure 7
- information architecture 7
- tone 4
- event semantics 2
- format 2

## Lead Candidate
必须通过 `LEAD_VALIDITY_GATE.md`。
只匹配 topology 的图只能作为 `STRUCTURE_ONLY_REFERENCE`。

## Support
最多 1 张，使用前必须写 `support_scope`，只能解决一个局部变量。

## Coverage Gap
找不到合法 Strong Lead 时：
- 可使用 Structure-only Reference 辅助布局；
- 但不得宣称“高度参考”；
- 若要进入全新 medium/value/type 世界，应选新 Lead 或走 Concept-led route。
