# H0 Reference Fidelity Gate v0.13

## 为什么新增这个门禁
v0.12 暴露了一个冲突：系统一方面要求 H0 必须“艺术字”，另一方面又要求强借 Lead Reference。结果模型会为了证明“有设计”而给标题加渐变、描边、发光、纹理，反而破坏参考图真正的字体人格。

因此 v0.13 将全局规则从“所有 H0 必须显眼艺术字”改为：

> **H0 必须经过明确设计，但设计方式必须由 Lead Reference / Style Pack 决定。**

## 1. H0 三种合法模式

### MODE A — REFERENCE_LED_DISPLAY_TYPE
当 Lead 的 H0 本身依靠成熟字体与排版关系成立时使用。

允许：
- 使用与 Lead 同类的真实字体骨架；
- 定制字号比例、字距、行距、纵排/横排、分栏、裁切、错位；
- 轻微 glyph-safe 字形修整；
- 让 H0 与 Hero 发生位置/遮挡/轴线关系。

不要求：
- 渐变填充；
- 手写化；
- 图像纹理塞进字里；
- AI 自由造字。

这仍然算“被设计过的 H0”，不是偷懒的普通字体放大。

### MODE B — GLYPH_SAFE_ARTWORD
当 Lead / Style Pack 明确依靠手绘字、变形字、插画字、粗笔字等作为视觉人格时使用。

要求：
- 真实字符骨架；
- 明确的笔画改造逻辑；
- 与 Hero 的线条 / 材质 / 概念至少共享 2 项特征。

### MODE C — IMAGE_INTEGRATED_H0
当 Lead 的标题与图像融合（字即物、图穿字、材质进入字形）时使用。

要求：
- H0 的图像融合是构图机制，不是后加滤镜；
- 去掉融合关系后 Concept 会明显坍塌。

## 2. H0 Type DNA 必须记录
生成前记录：
- skeleton_class: song/ming / sans / grotesk / serif / handwritten / custom
- stroke_contrast: low / medium / high
- weight: thin / light / regular / medium / bold / black
- width: condensed / normal / wide
- vertical_proportion: short / normal / tall
- terminal_personality
- arrangement: horizontal / vertical / grid / staggered / cropped
- fill_behavior: flat / outline / texture / gradient / image
- color_role
- effect_class: none / shadow / glow / stroke / bevel / etc.

## 3. 参考匹配硬规则
当 Lead 存在时：
- weight 跨越 2 级以上 → RED
- high-contrast → low-contrast 或反之 → RED
- flat solid → gradient/glow/3D，且 Lead 无证据 → RED
- light/narrow/tall → heavy/wide/chunky → RED
- single-color title → multi-color title，且 Lead 无证据 → RED
- Lead 为精致排印型 H0，却强行手写化 → RED

## 4. 禁止“为了主题化而乱加效果”
以下理由不能单独支撑 H0 效果：
- “敦煌有很多颜色，所以标题做渐变”
- “数字展，所以标题发光”
- “音乐，所以字像波形”

主题化优先进入：字形结构、位置关系、排版节奏、图字关系；不是先进入表面滤镜。

## 5. 失败判定
以下任一即 H0 FAIL：
- 只为了满足 Artword Gate 加了无依据的渐变/描边/发光；
- H0 的字体人格与 Lead 明显相反；
- 字形正确但视觉效果破坏整张图的风格统一；
- 仅凭“比普通字体更花”就声称更有设计感。
