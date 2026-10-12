# Typography Strategy Router v0.13

## 目标
让字体决策服从参考与视觉世界，而不是先决定“必须做艺术字”再加效果。

## 1. 先判断 Lead 的 H0 类型
### T1 — Editorial Display
特征：真实字体、比例/排版/位置构成视觉性。
→ 使用 `REFERENCE_LED_DISPLAY_TYPE`

### T2 — Handmade Artword
特征：手写、粗笔、儿童画、拼接字、明显自定义字形。
→ 使用 `GLYPH_SAFE_ARTWORD`

### T3 — Type/Image Hybrid
特征：图穿字、字成物、文字被材料化。
→ 使用 `IMAGE_INTEGRATED_H0`

## 2. 主题只决定“内容如何进入字”，不决定滤镜
可主题化变量优先级：
1. 字形比例与结构
2. 排列与阅读方向
3. 字与 Hero 的相交/嵌入
4. 文字出现的位置与尺度
5. 局部笔画替换
6. 材质/颜色效果（最低优先级）

## 3. 正文字体匹配
正文/英文/数字要从 Lead Type DNA 推导：
- serif contrast
- weight ladder
- width
- capitalization
- tracking
- numeral style
- vertical/horizontal behavior

## 4. 选择真实字体也可以是“设计”
如果 Lead 本身靠精确排印成立，选择与其 Type DNA 匹配的字体 + 定制结构排版，是正确设计，不应被 Plain-H0 Shortcut 误判。
