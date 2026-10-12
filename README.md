# 文化活动宣传海报生成 Skill

当前版本 **v0.19**。面向文化活动的参考驱动创意、两条以上设计路线、字体样张与艺术字、中文和英文 SVG 排版、最终图文叠加可读性检查。

> **项目边界：**这是一套规则 + Python 工具集，不是单命令全自动调用 AI 的生图服务。Prompt Compiler 不直接生成图片；最终交付需要视觉审核，不能依赖自动分数。

## 从哪里开始
- [SKILL.md](SKILL.md)：任务唯一入口与断点、交付步骤。
- [ACTIVE_RULE_INDEX.md](ACTIVE_RULE_INDEX.md)：当前规则优先级；旧版历史记录不能覆盖新门禁。
- [QA_ACCEPTANCE.md](QA_ACCEPTANCE.md)：质量分数、失败条件和视觉批准要求。
- [manifest.json](manifest.json)：v0.19 元数据、正式能力声明。

## 规范文档
- [参考与视觉保真](docs/REFERENCE_SYSTEM.md)：Lead、Support、结构/配色/媒介与三维差异审查。
- [字体与艺术字](docs/TYPOGRAPHY_SYSTEM.md)：H0 路线、字体许可、字符覆盖、中英字形样张。
- [设计、创意路线与用户反馈](docs/DESIGN_AND_ROUTES.md)：多方案、反通用模板、拒绝路线重选。
- [可选 LoRA](docs/OPTIONAL_LORA.md)：后端能力、许可、下载确认、基线 A/B。

## 核心资源
| 目录 | 内容 |
| --- | --- |
| `core/` | **46 个** YAML 配置（数值与状态以可执行配置为准） |
| `reference_library/` | **113 张**参考图，**10 个暂定视觉簇**；不等于 10 套风格包 |
| `style_packs/` | 当前 **1 套正式风格包** `S01_PLAYFUL_DOODLE` |
| `modules/prompt_compiler_v017/` | 仅编译路线/提示词，不进行真实生图 |
| `layout_engine_v018/` | SVG-first 混合可编辑排版与 v0.19 最终合成可读性质检 |
| `scripts/`、`schemas/` | 命令行脚本与契约 |
| `tests/`、`tests_v017/`、`audit/` | 测试与分版本审计证据 |

## 环境与常用命令
需要 Python 3.9+。核心工具按功能需要 Pillow、NumPy、fontTools、CairoSVG（部分系统另需 Cairo 图形依赖）。脚本和测试里的示例字体可能指向 Linux 路径，在 macOS / Windows 上须替换为本机有授权且含所需字符的字体；跳过测试不视为通过。

```bash
python scripts/preflight_brief.py examples/brief_complete.json
python scripts/compile_routes_v017.py <正式项目JSON> <输出目录>
python -m unittest discover -s tests_v017 -v
python -m unittest discover -s tests -v
python -m unittest discover -s layout_engine_v018/tests -v
python -m unittest discover -s layout_engine_v018/readability -p 'test_readability.py' -v
python layout_engine_v018/readability/audit_and_repair.py poster_plan.json --out-dir build/readability
```

生成 SVG 的直接输出仅为**候选预览**。可读性合格不等于最终视觉批准；需要真实看图、审查中英文并保存与最终 PNG SHA256 绑定的审核记录，详见 [质检模块](layout_engine_v018/readability/README.md)。

## 维护原则
每条可执行阈值仅在代码或 `core/*.yaml` 保留唯一权威定义，概念说明见 `docs/`，对外介绍见 README，流程见 SKILL。历史说明保留于 Git 提交历史，避免同主题 `*_GATE.md` 在根目录重复维护。

第三方参考图片、字体和模型须分别核查权利；仓库收录不自动等于可商用或可再分发。版本记录见 [CHANGELOG.md](CHANGELOG.md)。
