# v0.19 (2026-10) — Final Composite Readability Gate
- New executable `layout_engine_v018/readability/audit_and_repair.py` + local contrast, texture, protected elements and thumbnail checks.
- Actual full rendering → isolate under-text background → hard fail → style-bounded repair → re-render → re-audit → render-bound visual approval.
- Bounded local-tint drawing added to SVG compositor; existing SVG text stays editable.
- QA / SKILL / Active Rule Index / Poster Plan schema wired to one gate; no parallel general scoring system.
- Added four required failure scenarios and additional edge regression tests. Original Reference Library, LoRA and multi-route generator preserved.

## 0.16
- 在首轮 Hero Rough 前新增带结构化输入校验的 Prompt Compiler；为同一参考输出 A/B/C 方案。
- 参考是否真的经过观察和是否实际发送给后端分开记录；不再声称文本提示词已完成图像条件生成。
- 保留 LoRA，当前不支持后端走 BASELINE_ONLY；加强泛黄旧纸/图标贴纸/镜像素材等捷径防线。
- 提供一个从 P03 参考图到 Prompt 的可复现示例与 16 项静态测试，不宣称真实生图审美已验证。

# Change Log

## v0.14 — Brief & Model Adapter Integration
- Inserts P0/P1/P2 preflight into authoritative workflow before design/model search, with source trace and compact clarifying breakpoints.
- Defines capability-first `find_lora` selection with verified metadata, rights, explicit download consent, baseline A/B and non-LoRA fallback.
- Creates registry and backend capability contracts, S01 optional adapter preferences.
- Adds offline safety gate scripts + metadata-only Hugging Face candidate search + regression tests.
- Preserves original reference library, v0.13 Lead / Surface / H0 / QA gates.

## v0.13
See historical audit and case study for original reference-fidelity changes.

## v0.15 — Chinese Type Assurance
- Based on observed REF-097 vs v0.13 Dunhuang poster Chinese H0 mismatch.
- Added Type DNA blueprint, separate mechanical/visual gates, font-file cmap probe, specimen image renderer, browser-face audit, and safe font download breakpoint.
- Prevented Songti-by-name, CSS weight synthesis, ordinary-font-as-custom-display, and text-accuracy score inflation shortcuts.
