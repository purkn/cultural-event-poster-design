# Coverage Gap Policy v0.13

## HIGH >= 0.78
- 需要合法 Strong Lead；
- 2 roughs 默认。

## MEDIUM 0.52–0.77
- 比较至少 2 个 Lead Candidate；
- 每个 Candidate 先过 Lead Validity；
- 不把 topology-only 相似误报成完整 Lead。

## LOW < 0.52
- 允许 `STRUCTURE_ONLY_REFERENCE` 辅助布局；
- 若 medium/type/palette 无可靠来源，进入 concept-led extrapolation；
- rough_count >=3；
- 不得用 Support 拼成“平均风格”。

## 不降标准
Coverage Gap 只表示案例库不足，不表示：
- 可以放宽 Surface Fidelity；
- 可以随意用 AI 默认发光/渐变风；
- 可以降低 Design Score。
