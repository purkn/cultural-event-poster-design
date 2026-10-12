# v0.8 系统诊断 → v0.9

## 结论
v0.8 已经解决了“概念和画法一起乱变”的问题，但它仍然是**单风格测试逻辑**，不适合未来拥有多个 Style Pack 的系统。

## 问题 1：风格锁得太早
v0.8 把 Style Route 放在 Theme Insight 前面：先锁 `S01A_BOLD_ARTWORD`，之后才解释活动真正要表达什么。这会产生先入为主。

多风格系统中应该是：
`Brief + Assets + Audience + Format + Theme Insight → Style Candidates`
而不是：
`Style → 再解释 Theme`。

## 问题 2：把操作器覆盖率当成质量
“12 个概念使用全部 12 种操作器”容易诱导系统为完成覆盖率而发散，而不是为设计问题服务。

v0.9 改为：
- 先选“最相关的视觉机会”；
- 每个 Style Route 只调用 2–5 个高适配操作器；
- 禁止把 operator coverage 当成优秀指标。

## 问题 3：Theme Specificity 容易变成修辞
例如“蒸汽只属于咖啡”并不成立，热茶同样有蒸汽。真正的专属性不能靠语言辩护，而要通过结构测试。

v0.9 的 Theme Specificity 要求：
- 至少绑定 2 个独立活动维度；
- Swap Test：替换成邻近活动后是否还能原样成立；
- 禁止虚构“唯一性”。

## 问题 4：概念阶段没有真正纳入素材价值
文化活动海报的路线经常被素材决定：
- 高质量人物摄影 → 摄影/编辑路线可能更优；
- 古籍扫描 → 档案拼贴可能更优；
- 儿童画 → 不应该重画成 AI doodle；
- 没有好图片但标题很短 → 字体主视觉可能更优。

所以 Asset Audit 必须发生在 Style Routing 前。

## 问题 5：没有把“信息量”当作创意约束
一张概念图可能很酷，但最终还要放：日期、地点、主办、CTA、英文版本。v0.9 在 Concept Gate 新增 Information Accommodation 与 Bilingual Feasibility。

## 问题 6：不同 Style Pack 不应该用同一套绝对审美分数直接横比
不同风格需要：
- 各自的 reference-relative score；
- 再转换为 normalized style score；
- 最后和 universal poster score 合并。

否则严肃博物馆风和儿童涂鸦风会被错误地用同一“活泼度”标准比较。

## v0.9 新核心
**不是 Event Type → Style。**
而是：

`Design Context → Visual Opportunities → Style Candidates → Route Candidates → Internal Competition → Final Poster`
