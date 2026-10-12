# S01 Prompt Compiler v0.13

## Prompt 不从“手绘、可爱、奶油底”开始
必须先写：
1. 当前 Concept Embodiment（画面结构被什么机制改变）
2. H0 如何成为主视觉的一部分
3. Lead Reference 提供的抽象结构语法
4. 哪个素材被 ADAPT/TRANSFORM
5. 明确禁止 even icon ring / sticker sheet / generic cute

## Style Surface
之后才添加：
- hand-drawn mixed strokes
- marker / crayon / pen variation
- light warm paper or white base
- selective bright accents
- imperfect but controlled outlines

## Rough 要求
Rough 也必须锁定：
- H0 role
- dominant scale
- negative-space shape
- mark variation
- palette family
不能用“只是草图”作为风格漂移理由。


## v0.13 Reference Blueprint Inputs
当存在 Lead Reference 时，Prompt 必须显式写入：
- H0 target area ratio / placement
- palette role map（背景/主色/点色及面积）
- negative-space target region
- type-image relationship
- dominant scale relationship
- decoration budget
- typography personality

禁止只写“参考某某海报的手绘感/留白感”。

## Semantic Decoration Guard
除非 Blueprint / Concept 明确要求，不得自动加入太阳、云、草芽、音符、星星、笑脸等 filler。
