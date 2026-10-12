# 文化活动海报系统 v0.19

自主式文化活动宣传海报生成技能。从活动简报出发，经参考图检索、多路线 Prompt 编译、SVG-first 双语排版、最终合成可读性质检，交付可编辑的中英文竖版海报。

## 运行时入口

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 唯一任务协议，定义完整流水线与断点规则 |
| `ACTIVE_RULE_INDEX.md` | 规则优先级索引，所有门禁的执行顺序与短路条件 |
| `manifest.json` | 版本元数据、45 项核心特性清单、质量门禁阈值 |

## 主要目录

| 目录 | 内容 |
|---|---|
| `core/` | 42 个 YAML 规则定义（参考检索、配色门禁、字体 DNA、捷径防线等） |
| `layout_engine_v018/` | SVG-first 排版引擎 + 最终合成可读性审计/修复脚本 |
| `modules/prompt_compiler_v017/` | 多路线 Prompt 编译器，为同一参考输出差异化方案 |
| `reference_library/` | 113 张参考图、10 个视觉簇索引，供两阶段检索使用 |
| `style_packs/` | 风格包配置（当前含 S01_PLAYFUL_DOODLE），含正负参考图与路由参数 |
| `scripts/` | 命令行工具：路由编译、LoRA 门禁、字体覆盖检查、参考比对等 |
| `schemas/` | JSON Schema：Lead 有效性、参考蓝图、路线输入、字体蓝图等 |
| `model_adapters/` | 后端能力注册表与 LoRA 适配器配置 |
| `tests_v017/` | 纯标准库单元测试（19 项） |
| `tests/` | 集成测试（需 Pillow） |
| `audit/` | v0.19 质检证据（4 组可读性场景的渲染/审计报告） |
| `feedback_registry/` | 用户审美否定记录，优先于历史 Design PASS |
| `collaboration/` | 参考包格式规范与风格包交接文档 |
| `examples/` | 简报样例、参考蓝图示例、LoRA 候选模板 |

## 快速命令

```bash
# 运行路由编译器
python scripts/compile_routes_v017.py <输入JSON> <输出目录>

# 跑纯标准库测试
python -m unittest discover -s tests_v017 -v

# 参考图并排比对（需 Pillow）
python scripts/create_reference_comparison_v017.py \
  --lead <参考图.jpg> --generated <生成图.png> --out <比对结果.png>
```

## 依赖

- Python 3.9+
- `tests_v017/` 仅需标准库
- `tests/` 与 `layout_engine_v018/readability/` 需要 `Pillow` 和 `NumPy`
- LoRA 支持可选，需兼容外部后端；不支持时自动降级为 BASELINE_ONLY

## 质量门禁

| 指标 | 阈值 |
|---|---|
| Design 最低分 | 82 |
| Production 最低分 | 85 |
| 视觉证据 | 必须提供 |
| 最终合成可读性 | 阻断级（不通过不出图） |
| SHA256 视觉审批 | 必须 |

## 版本说明

本仓库当前为 v0.19（2026-10-12 入库）。旧版中文交互版 Skill 已从工作树移除，可从历史提交 `44ab75e` 恢复。

`SKILL.md` frontmatter 名称为 `cultural-event-poster-system`。若技能加载器要求目录名与 `name` 一致，请将本目录改名为 `cultural-event-poster-system`。
