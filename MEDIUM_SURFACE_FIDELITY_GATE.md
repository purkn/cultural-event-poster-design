# Medium & Surface Fidelity Gate v0.13

## 核心
参考图的“媒介人格”与“表面结构”不是次要细节，而是风格识别度的核心。

v0.12 的典型失败：Lead 是高明度、蓝白双色、版画/刻线式二维图形；生成结果却变成低明度、黑底、多色、发光、液态/分形式数字渲染。虽然都叫“流动”，但视觉世界完全不同。

## 1. Reference Blueprint 必须新增 Surface Fingerprint
- medium_class: print / engraving / woodcut / crayon / marker / collage / photo / painterly / digital_2D / digital_3D / generative_fractal
- dimensionality: flat / shallow / volumetric
- edge_behavior: crisp / rough / bleeding / soft / glowing
- mark_frequency: sparse / medium / dense
- dominant_mark: line / block / dot / photo-tone / gradient-field
- lighting_model: none / flat / diffuse / directional / volumetric
- surface_finish: matte / paper / glossy / luminous
- background_value_regime: high_key / mid_key / low_key
- texture_scale: fine / mixed / coarse

## 2. Lead Fidelity Hard Rules
Strong Lead 模式下，以下变化默认 RED：
- high_key ↔ low_key 反转；
- flat ↔ volumetric / 3D；
- line/print medium ↔ glossy generative liquid；
- matte/paper ↔ luminous/glossy；
- 双色/低色数 ↔ 多色发光渐变；
- dense mark-making ↔ smooth empty gradient field。

除非在进入 Rough 前就声明 `PARTIAL_BREAK` 并证明另一个 Lead 更适合，否则不允许生成后再解释。

## 3. Concept 不能覆盖 Medium
Concept 负责：
- 主体语义
- 视觉隐喻
- 主题转译

Lead 负责：
- 主要媒介人格
- 表面语言
- 色彩角色结构
- 字体人格

如果 Concept 需要彻底改变 Lead 的 medium，说明 Lead 选错了，应重新检索，不应硬做。

## 4. Surface Delta
最终必须比较：
- medium_class
- dimensionality
- background_value_regime
- color_count
- mark_frequency
- lighting_model
- surface_finish

其中 2 项以上 RED → Reference Delta 整体 RED。
