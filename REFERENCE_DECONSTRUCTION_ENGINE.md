# Reference Deconstruction Engine v0.13

## 目的
把参考海报拆成可执行的**空间结构 + 表面媒介 + 字体 DNA**，避免只学到“流动 / 极简 / 手绘”这种抽象标签。

## 1. 两阶段检索
### Stage A — Coarse Retrieval
用索引 / cluster / semantic tags 找 Top 12–20。

### Stage B — Fine Deconstruction
对 Top 6–8 做完整拆解，再重新排序。

## 2. Reference Blueprint 字段

### A. Spatial topology
- H0_bbox / hero_bbox / info_bbox[] / footer_bbox
- dominant_visual_center
- main_axis
- symmetry
- type-image relationship

### B. Area ratios
- H0_area_ratio
- hero_area_ratio
- information_area_ratio
- decoration_area_ratio
- negative_space_ratio

### C. Negative-space map
- high / medium / empty cells
- largest_contiguous_empty_region
- empty-region function

### D. Palette & value regime
每个角色记录：
- hue family
- area %
- saturation
- lightness
- contrast purpose

并记录：
- background_value_regime: high_key / mid_key / low_key
- chromatic_role_count
- dominant_color_count

### E. H0 Type DNA
- skeleton_class
- stroke_contrast
- weight
- width
- vertical_proportion
- terminal_personality
- arrangement
- fill_behavior
- color_role
- effect_class

### F. Supporting typography
- body family personality
- English personality
- numeric treatment
- tracking / alignment / line-height / case behavior

### G. Medium & Surface Fingerprint
- medium_class
- dimensionality
- edge_behavior
- mark_frequency
- dominant_mark
- lighting_model
- surface_finish
- texture_scale

### H. Mark / line language
- line_weight_mean
- line_weight_variation
- roughness
- edge type
- fill type
- stroke-to-fill ratio

### I. Crop & scale
- object_count
- dominant_object_count
- extreme_crop
- edge_breaks
- biggest-to-smallest scale ratio

### J. Decoration grammar
- motif category
- count
- scale class
- role

### K. Distinctive moves
至少 3 项“删掉就不再像这张海报”的动作。

## 3. 重新排序权重 v0.13
粗检索仅 25%。精拆权重 75%：
- topology 15
- medium_surface 14
- H0 Type DNA 13
- type-image relationship 10
- palette + value regime 10
- density/negative-space 8
- information architecture 3
- material/mark detail 2

## 4. Lead / Structure-only 判断
如果 topology 高但 medium/type/palette 低：标记 `STRUCTURE_ONLY_REFERENCE`，不能作为 Strong Lead。
