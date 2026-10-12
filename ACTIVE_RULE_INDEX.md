# Active Rule Index v0.19 — Authoritative Priority

1. `SKILL.md`（唯一任务协议）
**最终合成可读性质检（最高生产优先级）：** `layout_engine_v018/readability/README.md` + `layout_engine_v018/readability/audit_and_repair.py`；覆盖旧规则中把字体检查/溢出检查或主观视觉总分视为读字合格的捷径。
**排版/文本优先：** `layout_engine_v018/SVG_FIRST_LAYOUT.md` + `layout_engine_v018/H0_VARIATION_GUARD.md` + `layout_engine_v018/scripts/build_poster_svg.py`；覆盖旧版 HTML 唯一母版和默认逐字变奏假设。
**首轮生图前优先：** `ROUTE_RESELECTION_V017.md`、`PALETTE_AND_TYPE_DECISION_V017.md`、`modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md`、`VISUAL_QA_AND_SHORTCUT_AUDIT_V017.md`。这三项覆盖历史 rough 文字规则，不覆盖事实或 LoRA 许可门禁。
2. `BRIEF_INTAKE_BREAKPOINTS.md`（**新**，所有生图与下载前）
3. **`TYPOGRAPHY_ENGINE_V015.md`、`TYPE_SPECIMEN_SOP.md`、`FONT_DOWNLOAD_BREAKPOINT.md` + `core/chinese_typography_gate.yaml`（新增跨风格字体硬门禁）**
4. `MODEL_ADAPTER_LAYER.md`、`FIND_LORA_PROTOCOL.md`、`LORA_LICENSE_AND_DOWNLOAD_GATE.md`、`LORA_BENCHMARK.md`（**新**，仅 LoRA 支持时激活）
5. `LEAD_VALIDITY_GATE.md`、`LEAD_DOMINANCE_CONTRACT.md`
6. `REFERENCE_DECONSTRUCTION_ENGINE.md`、`REFERENCE_BLUEPRINT_CONTRACT.md`
7. `MEDIUM_SURFACE_FIDELITY_GATE.md`、`TYPOGRAPHY_STRATEGY_ROUTER.md`、`H0_REFERENCE_FIDELITY_GATE.md`
8. `PALETTE_STRUCTURE_GATE.md`、`EFFECT_DISCIPLINE_GATE.md`
9. `REFERENCE_DELTA_GATE.md`、`TYPOGRAPHY_REFERENCE_GATE.md`、`NEGATIVE_SPACE_GATE.md`
10. `DESIGN_QUALITY_CORE.md`、`QA_ACCEPTANCE.md`
11. `core/*.yaml` 与当前 Style Pack（若与上面冲突，按更高优先级）

## 强制短路与防捷径
- 内容 P0 不全 → WAITING_FOR_USER；不生图、不检索 LoRA。
- backend LoRA `false` 或 `unknown` → BASELINE_ONLY，不再发起 LoRA 下载申请。
- license 未核实/底模不匹配 → 拒绝 LoRA 候选，不发起授权下载。
- 无当次下载确认 → 不下载；同意下载一个模型不等于同意其它模型。
- 使用了外部 LoRA 却没记录证据、revision 和 adapter scale → 不得报告“已验证”。
- LoRA 结果与 Lead 媒介/配色/H0 DNA 冲突 → 关闭 LoRA，不能用“生成更漂亮”覆盖 RED。
- 缺 logo 与素材通常可继续，不能把“资料不足”当作不做工作的借口。
- 只有目录结构检查合格，不代表模型已经实际生图成功；未测实际推理不报真实稳定性。

- 中文 H0 未证明指定真实字体加载/字符覆盖或字形样张失配 → TYPOGRAPHY_UNRESOLVED，不得设计 PASS。
- 浏览器 CSS 字体家族字符串正确，不等于实际字体装载成功；必须保存字库路径与图像证据。

- 生图 Prompt 未经真实参考图观察、编译前检查 → STOP。
- 静态编译、字体加载、清除水印 ≠ Hero 质量评价；无真实 Rough 不能判设计 PASS。

## v0.17 执行优先级
1. 已收到的用户设计否定（项目 scoped） > Agent 所有历史高分和示例设计参数。
2. 已否定 route 不可直接复用；先构建至少两条真正不同的路线，再生成 prompt。
3. 原 v0.16 编译器不再处于运行目录；禁止搜索旧 compiled prompt 作为新任务输入。
4. 早期 rough 审美失败时直接返回 route，不要先处理字体/水印/HTML 再高分交付。

- 成图的文字与底图重叠，必须基于**最终渲染像素**对局部文字区计算可读性。未提交本轮 `readability_report.json` 与目标画面视觉复核，Production 不得 PASS。
- H0 / H1 低对比、覆盖重要主体、缩略过小 → 硬失败，不能用其它维度高分弥补。若修复失败只能回到布局/视觉阶段，不交付。
