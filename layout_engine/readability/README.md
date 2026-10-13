# Final Composite Readability Gate v0.19 (唯一可读性质检入口)

此模块**接在 SVG 母版生成之后、Production PASS 之前**；它不是另一套通用设计评分器。

## 审计对象 / 工作机制

- 以 Poster Plan 生成可编辑 SVG，并使用 CairoSVG 渲染**最终画面** `final_render.png`。
- 在同一 SVG 中隐藏文字、保留 hero/底色/所有装饰图层，另渲染 `pre_text_background.png`；再逐个渲染透明文字图层。三者来自同一版式、同一渲染器，计算的是文字**实际覆盖的局部像素**。
- 文字核心像素（alpha>0.62）测量 WCAG sRGB 相对亮度与对比度；对局部像素的第 10 百分位、达标比例进行判断，避免“整张海报平均很暗”误判局部浅底浅字。
- 对每个文字真实渲染框周边计算亮度标准差、梯度高频边缘密度，标记复杂纹理。默认将高复杂度弱关键信息判为硬失败；高复杂度但仍强对比的文本需要视觉复核，不得直接宣称审美通过。
- `protected_regions` 由视觉识别/人工标注的关键主体边界框（人脸、展品、品牌主物体）提供。检测重叠是几何可信的；**没有标注时不得宣称自动完成主体语义检查**。
- 25% 的缩略图检查标题 / 关键信息实际有效字号和亮度信号；并保留原始尺寸检查。**缩略判断是工程启发式，不等于真人阅读测试**。
- WCAG 大字（正常文字 >=24px 或粗体 >=19px）参照 3:1；其它文字参照 4.5:1。这是适用情况下的基线，**复杂图像海报并非被法律要求统一满足网站 WCAG**。

## 生产门禁（可收紧，不允许降低门槛）

| 指标 | 默认阈值 | 影响 |
|---|---|---|
| 局部 WCAG 对比 | 正文 4.5:1；大字 3:1 | `LOCAL_CONTRAST_FAIL` 硬失败 |
| 核心笔画像素达标比例 | >= 92% | 硬失败 |
| 文字核心像素局部对比第 10 百分位 | 不低于对应阈值 | 硬失败 |
| 局部背景纹理 | edge density >0.18 **或** luma std >0.205 | 若关键信息对比裕量小 → 硬失败；否则待视觉复核 |
| 25% 预览 H0 字号 | >= 12px | 不达标硬失败 |
| 25% 预览 Key 信息字号 | >= 7.5px | 不达标硬失败 |
| 25% 预览亮度信号中位数 | >= 0.095（亮度标量差） | 关键文字硬失败 |
| 关键主体重叠 | 文字渲染框与标注 protected region 超过自身 4% | 硬失败 |

这些阈值是**项目回归测试起点**，不是所有印刷/艺术字的通用审美真理。正文小字在 25% 缩略下不应被错误要求像 H0 一样可读；对其给警告，关键文字强制达标。

## 自动修复（按顺序，最多 2 轮）

1. **位置**：仅在原位置的相邻候选偏移测试（32/64px），且最大位移 6.5% 画幅、保证不撞其它文字/主体、不出安全区域。`lock_position=true` 的标题禁止移动。
2. **颜色**：只能选当前 Style / 设计方案明确允许的 `approved_text_colors`，不允许自动改成系统任意黑/白。
3. **局部底图**：仅当前 Style 授权 `allowed_treatments: [local_tint]` 时，可以尝试小面积淡色横向柔边遮罩（opacity <=0.16, 画布占比 <=10%），**禁止使用全页黑蒙层或厚重文字描边**，不得覆盖 `protected_regions`。当前执行器未提供 blur/局部照片修复的自动化；若这些操作确有必要，退回设计/素材阶段，不以文档代替实现。
4. **整体构图**：前三项无效、或无安全修复路线时输出 `must_escalate_layout=true`，返回版式选择/主视觉位置重排，**不强行交付**。

每次候选修复都实际重新渲染+重新测量；如果引入其它新 FAIL，则拒绝此次修复。最多两轮修复。审美修复（尤其局部蒙层）还须对照 Style / Lead 由具备看图能力的 Agent 复核。

## 最终视觉批准不是自评分

脚本先产出 `poster_final_review.svg`、`final_render.png`、`thumbnail.png`、`pre_text_background.png`、`poster_plan_review.json` 和 `readability_report.json`。技术 PASS 仍不允许正式交付；有看图能力的评审实际检查当前图像后，按下方完整协议提交 `--visual-review review.json`。

视觉证据必须对应当前 PNG/缩略图与所列文件哈希。不能把模型编造的“85 分、通过”冒充真实看图；无法看图时保持 `PENDING`，仅交候选稿及待验证报告。

## 命令（需 Pillow、NumPy、CairoSVG、fontTools，且图像渲染器能使用指定字体）

```bash
python layout_engine/readability/audit_and_repair.py poster_plan.json \
  --out-dir build/readability --max-rounds 2
# 视觉代理查看 build/readability/final_render.png，填写准确 SHA256 的 review.json：
python layout_engine/readability/audit_and_repair.py poster_plan.json \
  --out-dir build/readability --max-rounds 2 --visual-review build/readability/review.json
```

第二条命令会重跑确定性渲染、对比 SHA256；审查者对**一张实际 PNG**和前后背景进行视觉核查。

`status: REVIEW_REQUIRED` 说明强对比但复杂，需要视觉确认；`technical_readability_gate: FAIL` 不得被人工打分覆盖。

**限制**：只能自动检测本系统保留为 SVG text/path 的文字；无法单靠像素验证 AI 直接画在 hero 位图里的伪文字或其真实语义。位图内的正式信息不受支持，仍必须在 SVG 文字层重建。复杂渐变文字、CSS 滤镜、叠加模式或外部 SVG 编辑未重回渲染流水线时，需专门适配或判 `UNVERIFIED`。预览器 CairoSVG 与目标客户端渲染字体不完全一致时，必须进行最终目标渲染器复检。

## 最终评审协议

复制本目录 `visual_review_template.json` 到项目目录。按 [质量与交付规范](../../docs/QUALITY_AND_DELIVERY.md) 在真实看图后填写上下文、材料 path/SHA256、逐项预检、反默认套路的语境判断、分项评分与问题复验。旧版只含五段观察的审批不再足够。

每次最终渲染输出 `thumbnail.png`（默认 25%）及其 SHA；`readability_report.json` 另含 `review_issues/design_score/production_score/poster_plan_sha256`。技术 PASS、完整评审 PASS 和当前图像证据同时成立，才允许正式交付。参考对照可用 `python scripts/create_reference_comparison.py --lead lead.jpg --generated final.png --out comparison.png` 构建；工具只生成对照材料，不替代看图。

CLI：像素失败退出 3；指定 `--visual-review` 但评审未通过退出 4；无 review 的技术预检通过退出 0，但 `final_delivery_allowed=false`。材料与分项审美理由由评审负责，验证器不自动识别“好看”或认证看图行为。

评审中的 `poster_plan` 指向本轮输出 `poster_plan_review.json`，与当前最终图和缩略图一起绑定，不能引用修改前的旧 Plan。
