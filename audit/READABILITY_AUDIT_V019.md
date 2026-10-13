# v0.19 图文叠加可读性专项审计：根因、修改及边界

## 根因（实际对照上传的 v0.18）
1. [layout_engine/scripts/build_poster_svg.py](../layout_engine/scripts/build_poster_svg.py) 原本只做文字位置、文字间碰撞、字库覆盖和区域越界等静态几何检测，并未检查文本与图像像素叠加后的明度差及底图复杂度。运行成功时只报告结构 PASS，不含可读性 PASS。
2. `QA_ACCEPTANCE.md` 将 readability/overflow 放入 Production 分项 15 分，却未明确局部阈值或关键文字硬失败，因此整体分数可能盖过难读文字。
3. `SKILL.md` 的“最终目检”是自然语言要求，没有可执行的局部采样/定位/有限重试/再渲染闭环，也没有每段文字的证据链。
4. `SVG_FIRST_LAYOUT.md` 仍未把文本与 hero 的叠加干扰纳入结构生成器，允许在图像高频复杂区放文字而不报错。
5. 高层旧门禁很多，但没有一个针对最终叠字像素的权威产线入口；缺少失败后的安全修复器，修复依赖 Agent 反复微调。存在评分自证和跳过复检捷径。

## 本次最小必要接入
- 历史范围：当时保留 v0.18 SVG-first 和 Prompt Compiler v0.17；参考库与生成路径的当前状态见根 README。
- SVG 生成器只新增受控 `local_readability_treatments` 绘制能力及清晰 DRAFT 状态。
- 同一 Layout Engine 内新加 [audit_and_repair.py](../layout_engine/readability/audit_and_repair.py)（成图独立层渲染、像素局部度量、受控修复、重渲染、复检、出证）。
- 原 `SKILL.md` 的生产流水线步骤 L 更新为 Final Composite Readability，原 QA 分数不变但变为不可被补偿的硬门禁。`ACTIVE_RULE_INDEX.md` 赋予唯一权威入口。
- `poster_plan.schema.json` 新增可选的 style-approved 颜色、弱局部遮罩预算和重要主体保护框。

## 防偷懒 / 防安全感
- 不允许凭整图平均明度、CSS 填色、字库覆盖或自动 87 分“推断”可读性。
- 不允许通过把 WCAG 基准设为 1:1、把缩略比例调大、无限重试获得虚假 PASS：检测器拒绝弱化阈值与 >2 次修正。
- 自动移动只能在设计允许的小范围内，自动改色必须来自显式批准色表，局部背景 tint 的覆盖范围/面积/不透明度全部限额；没有其它授权时直接失败。
- 无主体保护区时标记“语义显著性尚未经机器验证”，最终必须视觉复核。即便对比达标，也不能声称艺术审美已通过。
- `final_delivery_allowed` 必须同时满足硬性指标 + **绑定最终 PNG SHA256** 的真实视觉复核。无复核证据只能交候选图和报告。

## 限制与未来改进
- 自动对比测试目前由本地 CairoSVG 引擎渲染，目标客户端字体和 SVG effect 支持可能不同；需要最终目标渲染器测试。
- 仅检测实际 SVG 文本或 SVG 定制轮廓。AI 生成到位图里的文字并不是可信的正式文案图层。
- 纹理和缩略信号为可复现工程指标，不能代替设计师/视觉模型对语义焦点和审美关系的评价。
- `local_tint` 已实现；高风险背景模糊、智能避人脸、复杂局部重绘**未实现**，本次不假装自动完成，统一返回布局/素材重设计。

## 测试要求
参见 [layout_engine/readability/test_readability.py](../layout_engine/readability/test_readability.py)：浅底浅字、深底深字、复杂高频、明暗不均 + 受保护主体、缩略图、蒙层授权约束、SHA256 防旧审阅和弱化阈值拦截。
