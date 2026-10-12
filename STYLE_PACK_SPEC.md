# Style Pack Spec v2.4

## Style Pack 与 Reference Cluster
- Reference Cluster：用于检索，可以临时、稀疏、混杂。
- Style Pack：经过验证的生成系统，必须完整可路由、可生成、可评估。

## 必须包含
```text
STYLE.md
router_profile.yaml
style_fingerprint.yaml
asset_affinity.yaml
operator_affinity.yaml
hero_grammar.yaml
h0_strategy.yaml
typography_map.yaml
layout_affinity.yaml
negative_rules.yaml
evaluator.yaml
prompt_compiler.md
references/
  anchors.json
  positive/
  negative/
failure_cases/
tests/
```

### 条件文件
若该风格使用 Handmade / Custom H0：
`artword_grammar.yaml`

若该风格使用 Editorial Display H0：
可增加 `display_type_grammar.yaml`。

## h0_strategy.yaml 必须说明
- default_mode: REFERENCE_LED_DISPLAY_TYPE / GLYPH_SAFE_ARTWORD / IMAGE_INTEGRATED_H0
- eligible_modes
- Type DNA 范围
- 何时允许效果
- 何时必须 flat / restrained
- 中文 glyph accuracy 策略

## retrieval_signature
每个 Style Pack 必须说明：
- 最适合的 topology / asset structure
- H0 条件
- medium/surface 特征
- background value regime
- 信息密度范围
- 适用/不适用 tone
- 常见误路由对象

## evaluator 必须包含
- style-relative criteria
- medium/surface fidelity
- H0 reference fidelity
- safe-template exceptions
- reference evidence requirements

## Promotion Gate
至少：
- 8 张正向参考
- 4 张 core anchors
- 4 个 regression briefs
- 2 个 failure cases
- 完整文件结构
- Router discrimination test 通过

## v2.4 新增：Reference World Compatibility
每个成熟 Style Pack 必须说明：
- 哪些 anchors 可做 Strong Lead；
- 典型 Surface Fingerprint；
- 典型 H0 Type DNA；
- palette/value profiles；
- negative-space / information architecture；
- 哪些 effects 默认禁止。
