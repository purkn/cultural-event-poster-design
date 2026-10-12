# v0.19 final composite readability update

详见 `layout_engine_v018/readability/README.md`、`audit/READABILITY_AUDIT_V019.md`；保留 v0.18 SVG-first、v0.17 多路线 Prompt Compiler 及 LoRA 备用分支。

> **v0.18 排版优先更新：** 新增 `layout_engine_v018/`，采用 SVG-first editable composition，禁止无依据逐字尺寸变奏，详见 `layout_engine_v018/README.md`。

# Cultural Event Poster Skill v0.17

**Default entry: `SKILL.md`, `ACTIVE_RULE_INDEX.md`, `ROUTE_RESELECTION_V017.md`**.

## This release fixes
- Production prompts inheriting the built-in fermentation example's fixed cyan/red/warm-paper palette.
- Reusing ZCOOL KuaiLe because the font had been installed, even after explicit negative aesthetic feedback.
- Pretending three variations of the same Lead/palette/typography are three different creative directions.
- Treating technical correctness (font cmap, watermark, layout) as proof of design quality.

This is an autonomous poster creation skill, not a human-in-the-loop art-director workflow. Breakpoints remain only for missing essential brief facts, font/model downloads, permissions/costs or non-automatable verification constraints. No paid API required by this release. LoRA support remains optional for compatible external backends.

### Main command
`python scripts/compile_routes_v017.py <PROJECT_PRODUCTION_INPUT_JSON> <PROJECT_OUTPUT_DIR>`

For input shape see `modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md`; sample JSONs are **not** a production source of defaults.

### Tests
`python -m unittest discover -s tests_v017 -v`

### Side-by-side image proof (Pillow)
`python scripts/create_reference_comparison_v017.py --lead <reference.jpg> --generated <hero.png> --out <comparison.png>`

This version is tested as a compiler and workflow package; it has not yet produced an actual aesthetically verified new poster. Do not report an automated design score from the compiler.

---

## 仓库版本更新记录

### v0.19 入库（2026-10-12）

`cultural_event_poster_skill_v0_19.zip`（382 个文件，约 50 MB）已完整解压并作为当前版本置于仓库根目录，包内文件保持逐字节原样，未做裁剪。

新增的主要目录：`core/`、`scripts/`、`modules/`、`schemas/`、`layout_engine_v018/`（含 `readability/audit_and_repair.py`）、`style_packs/`、`reference_library/`（113 张参考图，10 个视觉簇）、`model_adapters/`、`case_studies/`、`audit/`、`feedback_registry/`、`collaboration/`、`tests/`、`tests_v017/`、`archive/`。

本仓库原有的中文交互版 Skill（`SKILL.md`、`README.md`、`agents/`、`evals/`、`examples/`、`references/`，共 11 个文件）已从工作树删除，不再作为运行时入口；需要回看时从历史提交 `44ab75e` 取出。

运行时入口以 v0.19 为准：`SKILL.md`、`ACTIVE_RULE_INDEX.md`、`manifest.json`。

依赖说明：`tests/` 与 `layout_engine_v018/readability/` 需要 Pillow 与 NumPy，缺失时会 import 失败；`python -m unittest discover -s tests_v017` 为纯标准库测试。

注意：`SKILL.md` 的 frontmatter 名称已变为 `cultural-event-poster-system`，若技能加载器要求目录名与 `name` 一致，需要把目录改名为 `cultural-event-poster-system`，或让加载器以 frontmatter 为准。
