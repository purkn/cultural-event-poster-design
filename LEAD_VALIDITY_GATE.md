# Lead Validity Gate v0.13

## 核心问题
某张参考可能只在“构图结构”上很像，但媒介、色彩、字体人格与目标方向完全不同。它不能被称为 Lead。

## Lead 必须至少在 4 类中有 3 类达到 MEDIUM 以上匹配
1. spatial_topology
2. medium_surface
3. typography_DNA
4. palette_value_regime

若仅 topology 强匹配，其余弱：
- 标记为 `STRUCTURE_ONLY_REFERENCE`
- 只能辅助布局
- 不得作为 Strong Lead

## Strong Lead 最低要求
- topology >= 0.70
- medium_surface >= 0.65
- typography_DNA >= 0.60
- palette_value_regime >= 0.60
- overall >= 0.68

## 重新路由条件
如果为了当前 Concept 预计需要突破以下 2 项以上：
- background value
- medium
- H0 Type DNA
- palette role count
- main axis
- type-image relation

则必须重新选 Lead，不允许先生成再解释。
