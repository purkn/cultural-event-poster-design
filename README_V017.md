# 文化活动海报 Skill v0.17 — 失败路线重选，而非继续微调

这次更新针对用户连续明确否定的「美味发酵节」稿件，既包含文字规则，也包含可执行的路线编译器和测试。它不是一套新默认配色，也没有保证自动生成美观海报；它先防止失败的配色/字体/构图被再次照搬。

**关键修复**
1. **REF/EXAMPLE FIREWALL**：v0.16 发酵节样例曾同时承担测试素材与任务默认值，v0.17 将旧模块及其固定蓝红/米白配色移出运行时；任何新的生产输入必须显式构造，不能指向 sample/golden/demo 路径。
2. **REJECTED ROUTE REGISTRY**：用户明确表达不满意时，高于 Agent 自评。禁止把同一 Lead + 同一色系 + 同一字体 + 同一视觉母题当作“新版”。负反馈只对该项目生效，不是禁止所有活动使用蓝色。
3. **ROUTE BEFORE PROMPT**：要求有 2 条有证据的候选设计路线，不再把同一参考的 Prompt A/B/C 当成风格探索。每条路线独立选择 Lead、配色系统、媒介、H0 设计方法和构图概念；若缺合格路线，输出 NEED_NEW_ROUTE，不强行生成。
4. **COLOR / TYPE PROVENANCE**：颜色只能来自实际可观察参考/用户素材/明确艺术指导。缓存的旧字体≠合格字体；被否定的 H0 不能复用。不能用“已装好”“cmap PASS”证明美感。
5. **VISUAL FIRST**：先以低成本 rough 比较配色/媒介与主形，再排版；用户否定过的稿件标为 DESIGN_FAIL。没有生成截图证据不得给 Design PASS。
6. **保持 LoRA 双路线**：在外部 LoRA 不支持时正常走 BASELINE_ONLY；其它后端仍可按原有许可和下载断点走 LoRA。

**操作入口**：首先读取 `SKILL.md`、`ACTIVE_RULE_INDEX.md`、`ROUTE_RESELECTION_V017.md`、`modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md`。代码入口 `scripts/compile_routes_v017.py`，参考 `modules/prompt_compiler_v017/examples/README.md`。示例绝不作为任务默认值。

**如何验收**：`python -m unittest discover -s tests_v017 -v`；参考/成图比对脚本 `scripts/create_reference_comparison_v017.py` （需 Pillow）；只检查风格偏差证据，不做客观“漂亮分”。
