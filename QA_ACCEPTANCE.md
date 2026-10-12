# QA Acceptance v0.19（沿用 v0.15 双轴评分，新增成图可读性硬门禁）

## A. Hard Gates
任一失败不得交付：
- Mechanical factual error
- H0 character incorrect
- Lead Validity fail
- Lead Dominance / Support Scope fail
- Reference Blueprint missing
- Medium/Surface Fidelity RED
- H0 Reference Fidelity RED
- Palette Structure fail
- Effect Discipline fail
- Concept Embodiment fail
- Reference Delta RED without predeclared justified PARTIAL_BREAK
- Severe semantic-decoration shortcut
- Severe safe-template fail
- Unusable information layout

## B. DESIGN SCORE — 100
- Concept embodiment 12
- Lead blueprint structural fidelity 12
- Medium/surface fidelity 12
- H0/typography reference fidelity 12
- Type-image integration 10
- Composition & visual tension 10
- Palette/value structure 9
- Asset transformation 7
- Non-genericness/effect discipline 6
- Information architecture 4
- Negative-space intention 3
- Theme specificity 3

PASS >= 82

## C. PRODUCTION SCORE — 100
- factual accuracy 20
- H0 character accuracy 15
- readability / overflow 15
- information completeness 12
- image cleanliness 10
- format / resolution 10
- bilingual consistency 10
- mandatory asset correctness 8

PASS >= 85

## D. Evidence Gate
- 未目检最终图：Design <=60
- 有 Lead 但无 Structure+Surface+Typography Delta：Design <=70
- 无 Surface Fingerprint：Medium score <=4/12
- 无 H0 Type DNA：Typography score <=4/12
- 无 Support Scope 记录却用了 Support：Design Fail

## E. Score Honesty
技术无错、字全对、无水印，只能提高 Production；不能补偿视觉风格失配。

## F. v0.15 字体门禁（新增 Hard Gates）
- 没有实际 font file / face provenance（或没有完成授权下载）、H0 所需汉字缺失 → `TYPE_GATE_TECH FAIL`。
- Lead 定制字被替换为普通系统字体但未做样张比较及明确说明 → `TYPE_GATE_VISUAL RED`。
- 没有 HTML/CSS 渲染证据，不得声称浏览器无 fallback。
- 无中文 H0 参考裁片 + 候选 proof + 最终成图的三方对照：H0/typography 设计项封顶 40%。
- 未完成 TYPE_GATE_TECH 不可 Production PASS；未完成 TYPE_GATE_VISUAL 不可 Design PASS。
- 中文、英文分别过检。二者任何一个标题失败，交付 FAIL。


## G. v0.19 FINAL COMPOSITE READABILITY — Production hard gate（权威）
- **检测对象**：最终 SVG 合成图的实际 PNG，与同渲染器的 pre-text 背景/单独文字掩膜；严禁只检查 CSS 参数或全图平均色。
- **必须执行**：`python layout_engine_v018/readability/audit_and_repair.py poster_plan.json --out-dir build/readability`；再由具备看图能力的代理审查最终 PNG，提交按 SHA256 绑定的审查 JSON；审查器验证后才能填 `final_delivery_allowed=true`。
- **明度门槛**：大字 3:1、一般文字 4.5:1；核心字像素中 >=92% 满足门槛且 q10 对比不低于门槛。关键文字不达标直接 FAIL，不降级成扣分。
- **复杂度与显著性**：局部纹理/亮度变化、文字与受保护主体重叠、原尺寸和 25% 视图下关键信息的可见字号/亮度信号。复杂背景弱可读即 FAIL，强对比但纹理过多必须 `REVIEW_REQUIRED`。
- **修复上限**：最多 2 次真实迭代；只允许风格授权的小幅移动/颜色/局部柔边淡色处理。失败返回重排，不得自动全屏黑蒙层/粗描边/强投影。
- **记录格式**：每个文字块保留 `text, bbox_px, contrast_q10, contrast_pass_fraction, luminance_std, edge_density, thumbnail_signal, reasons, change_log, repair_history`。
- 15 分 `readability_overflow` 项并非硬门槛替代；未通过技术可读性或最终视觉复核时即使 Production 总分 >85 也不能交付。
- 重要语义视觉遮挡需要标注 `protected_regions`，无标注不可声称已自动识别人脸/展品。商业字体渲染器与最终端不同时须核查目标端。
