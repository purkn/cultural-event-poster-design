# 有效规则索引（v0.19）

## 权威顺序
1. `SKILL.md`：唯一运行总协议，活动事实与用户否定优先。
2. `BRIEF_INTAKE_BREAKPOINTS.md` 与 `scripts/preflight_brief.py`：资料 P0 缺失时先停机，不虚构。
3. `docs/REFERENCE_SYSTEM.md`、`docs/DESIGN_AND_ROUTES.md`：Lead/Support、构图媒介色彩与新路线；具体参数从 `core/*.yaml` 读取。
4. `docs/TYPOGRAPHY_SYSTEM.md`、`core/chinese_typography_gate.yaml`：真实字库/授权/字形视觉证明；不以字体文件存在冒充审美合格。
5. `modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md` 与 `scripts/compile_routes_v017.py`：编译真正不同的路线，不直接生图。
6. `docs/OPTIONAL_LORA.md`：可选支路；后端不支持即 BASELINE_ONLY。
7. `layout_engine_v018/SVG_FIRST_LAYOUT.md`、`layout_engine_v018/H0_VARIATION_GUARD.md`、SVG 构建器：排版与结构候选。
8. `layout_engine_v018/readability/README.md` 与 `audit_and_repair.py`：**最终合成可读性唯一权威执行入口**，失败不能交付。
9. `QA_ACCEPTANCE.md`：设计与生产评分及完整交付硬门禁；用户反馈、最终图 SHA256 视觉批准不能被总分抵消。
10. Style Pack 与 `core/*.yaml`：风格具体参数与可执行配置；配置和文件不一致时暂停核实，不凭旧版说明擅自补救。

## 强制停机规则
- 活动事实 P0 不完整：`WAITING_FOR_USER`。
- 没有观察实际参考图却声称参考忠诚：停止并取证。
- 用户已经否定的路线：重选 Lead/配色/字体/视觉机制；不能微调后自评通过。
- 字体无真实授权或核心字形不匹配：`TYPOGRAPHY_UNRESOLVED`。
- 后端不支持/未知 LoRA：`BASELINE_ONLY`，不下载模型。
- 没有生成真实 rough：`NOT_VISUALLY_REVIEWED`。
- 技术可读性 FAIL：退回排版和素材；对比阈值不可调低蒙混过关。
- 未实际目视最终 PNG 或缺少与 PNG SHA256 对应的复核：不得报告正式交付 PASS。

## 维护纪律
每一条可执行阈值只在代码或 `core/*.yaml` 内维护，根目录不再并存同主题的多个 *GATE.md。历史详情通过 Git 提交历史访问。参考拆解权重以 `core/reference_deconstruction.yaml` 为准，不继续引用早期不同分配方案。
