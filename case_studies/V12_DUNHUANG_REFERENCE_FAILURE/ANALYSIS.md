# V12 敦煌数字沉浸展失败案例

## 结论
该案例虽然 v0.12 自评 Design 88，但按 v0.13 应判 **FAIL**。

## 1. 思考过程中的关键错误
### 错误 A：Lead 只在 topology 上匹配
REF-105 的核心世界是：高明度、蓝白双色、平面密集刻线/版画感、白色细高对比竖排标题。
生成稿却是：低明度黑底、多色、发光、体积感、数字分形/液态材质。
这说明 REF-105 至多是结构参考，不应在不保留 medium/type/palette 的情况下被称为 Strong Lead。

### 错误 B：Support REF-068 实际覆盖了 Lead
“弥散柔光”不仅解决一个局部缺口，而是把：
- background value
- medium
- lighting
- chromatic count
- atmosphere
全部改了。
按 v0.13 属 Support Override Hard Fail。

### 错误 C：H0 Artword Gate 诱发了无依据渐变
参考 H0 是轻、窄、竖向、高对比、白色 flat solid。
生成 H0 是重、宽、大、每字多色渐变。
“敦煌有颜色”不能证明渐变标题合理。
正确策略应为 REFERENCE_LED_DISPLAY_TYPE，而非强制做渐变艺术字。

### 错误 D：Delta Gate 太宽松
v0.12 将背景明度反转、主色相扩宽、材质柔化记为 AMBER。
实际上：
- high-key → low-key = RED
- flat engraving → luminous generative = RED
- flat white H0 → multi-color gradient H0 = RED
整体必须 FAIL。

### 错误 E：评分膨胀
Production 做得干净不代表 Design 成立。
该稿技术正确，但参考世界严重漂移，不可能得到 88 Design。

## 2. H0 为什么怪
- 字重比参考重太多；
- 字面宽、体量厚，视觉气质从“诗性/编辑”变成“展览商业标题”；
- 每字渐变造成阅读节奏割裂；
- 渐变色又与复杂背景抢色；
- 参考的 H0 用“形态克制 + 白色反差”成立，生成稿却用“颜色效果”证明设计感。

## 3. v0.13 回归要求
再次执行此 brief 时：
- 若 REF-105 为 Strong Lead，必须保持 high-key + flat/print-like + low-color count；
- H0 必须采用轻/高对比/竖排/flat solid 的 Type DNA；
- 敦煌矿色可进入 Hero pattern，但不能自动灌入 H0；
- 若坚持 dark immersive glowing route，则必须重新选择与其 medium/value/type 匹配的 Lead，不得继续声称 REF-105 是 Lead。
