# 文化活动宣传海报设计 Skill

**版本：v0.19｜参考图驱动、多路线主视觉探索、双语 SVG 排版与可读性质检**

本仓库是供 AI Agent 和设计人员使用的**设计工作流与 Python 工具集**，不是自行调用图像模型的一键生图服务。核心优势是：从活动 Brief 与参考图构建可追溯的视觉路线、以 SVG/JSON 做中英文字排版，最终按实际叠字画面检查文字可读性，并要求真实视觉复核。

## 快速入口

| 想做什么 | 读取 |
| --- | --- |
| 理解 Skill 的生产流程 | [SKILL.md](SKILL.md) |
| 确定唯一有效的规则顺序 | [ACTIVE_RULE_INDEX.md](ACTIVE_RULE_INDEX.md) |
| 检查活动信息和素材授权 | [Brief 与素材规范](docs/BRIEF_AND_ASSETS.md) |
| 参考图检索、拆解、忠实度 | [参考图系统](docs/REFERENCE_SYSTEM.md) |
| 创意路线、颜色、装饰与反套路 | [设计与路线](docs/DESIGN_AND_ROUTES.md) |
| 艺术字、中英字体与字形技术检查 | [字体系统](docs/TYPOGRAPHY_SYSTEM.md) |
| 图文可读性与最终质量验收 | [质量与交付](docs/QUALITY_AND_DELIVERY.md) |
| 可选 LoRA 后端与许可证 | [LoRA 规范](docs/OPTIONAL_LORA.md) |

## 代码与素材分工

`core/`：**46 份 YAML 配置**（不是 42 份）；`scripts/`：预检、字体、模型与参考比较脚本；`modules/prompt_compiler_v017/`：多路线提示词编译器（只生成 Prompt，不自行调用生图 API）；`layout_engine_v018/`：SVG 排版及 v0.19 合成图可读性质检；`reference_library/`：113 张参考图、10 个暂定 cluster；`style_packs/`：当前正式风格包仅 **S01_PLAYFUL_DOODLE 一套**；`schemas/`：数据契约；`audit/`：本版审计与历史记录；`tests/`、`tests_v017/`：回归测试。

## 安装与初步校验

建议 Python 3.9+。需要运行图文可读性模块时，安装 `Pillow`、`NumPy`、`CairoSVG`、`fontTools`；不同操作系统可能需要 CairoSVG 系统图形库。示例 Poster Plan 含测试机的字体绝对路径，应改为本机存在且许可明确的字体文件。

```bash
python -m pip install Pillow numpy cairosvg fonttools
python -m unittest discover -s tests_v017 -v
python -m unittest discover -s tests -v
python -m unittest discover -s layout_engine_v018/tests -v
python -m unittest discover -s layout_engine_v018/readability -p 'test_readability.py' -v
```

部分测试使用 Linux 字体路径，其他平台需适配或可能跳过/失败；不可把跳过称为通过。**本仓库目前没有经过独立证明的一键端到端真实生图保证。**

```bash
# 预检活动信息
python scripts/preflight_brief.py examples/brief_complete.json

# 正式项目 JSON 须自行准备，不能直接用 examples 充当生产输入
python scripts/compile_routes_v017.py project.json build/routes

# 先将示例 JSON 的 font_file 修改为本机有效路径
python layout_engine_v018/scripts/build_poster_svg.py layout_engine_v018/examples/example_plan.json build/poster.svg --png build/preview.png

# 对真实 Poster Plan 的成图执行像素可读性审计
python layout_engine_v018/readability/audit_and_repair.py poster_plan.json --out-dir build/readability
```

编译、SVG 预览与最终可读性是不同阶段；**不经 `--visual-review` 且未绑定最终 PNG SHA256 时，只能称候选稿，不是正式通过的交付物**。具体证据流程详见 [可读性模块说明](layout_engine_v018/readability/README.md)。

## 版权与使用边界

参考图库包含来自第三方的视觉素材；入库不意味着已获商业、改编或再分发许可。权属未核实前不得默认商用。仓库未提供统一明确的许可证时，不能推定代码、素材和字体可以自由再分发。旧版文档曾以不同数值解释同一规则，现已合并为当前文档；历史详情通过 [CHANGELOG.md](CHANGELOG.md) 与 Git 提交追溯。
