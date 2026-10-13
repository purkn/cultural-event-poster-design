# 文化活动宣传海报设计 Skill

**版本：v0.20.2｜参考图驱动、多路线主视觉探索、双语 SVG 排版与可读性质检**

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

## 文件结构与职责

```text
SKILL.md / ACTIVE_RULE_INDEX.md  流程入口与规则优先级
manifest.json                   当前版本、模块与参考库清单
docs/                           5 份主题规范：简报、参考、设计、字体、交付
core/                           45 份按职责拆分的 YAML 规则与阈值
scripts/                        预检、参考库维护、提示词编译、字体与对照图工具
modules/prompt_compiler/         当前使用的提示词编译器及输入示例
layout_engine/                  当前使用的 SVG 排版引擎、像素可读性质检与测试
reference_library/
  collections/keyword-20261012/  唯一当前批次：401 张原图及权威 manifest
  index.json / index.csv        401 条派生索引，JSON 用于程序、CSV 便于人工检查
  facets.json / coverage.json   四维关键词检索与库存统计
  aliases.json                  113 个旧 ID 到新 ID 的映射，不重复存图
  review_queue.json             16 张未知标签图片的待复核清单
  previews/                     可重建的接触表与离线图库
schemas/                        输入和视觉证据的数据契约
examples/                       活动与 Blueprint 示例，不作正式生产输入
feedback_registry/              项目专属否定反馈，避免再次生成被拒绝路线
collaboration/                  外部参考素材交接格式
tests/                          当前规则、字体、参考库和编译器回归测试
audit/                          保留最终可读性测试证据；历史报告从 Git 查询
```

### 为什么只保留 401 张

“400 张”是近似称呼：新批次实际为 **401 张不同图片**。逐张 SHA256 校验确认，旧 113 张全部包含其中。此前分开存放是为兼容旧路径，造成 514 个原图文件和 514 条记录；本次删除旧副本、旧批次及旧视觉簇，统一使用新批次。旧 ID 与新 ID 的数字不代表同一张图，必须经 `aliases.json` 定位新 ID，再查询其 `image_path`。旧磁盘路径不再支持。

按用户要求移除整个 S01 风格包和专用样本，示例与编译器测试改用统一图库。S01 样本并非新图库的字节级重复；删除目的是取消独立预设体系。参考主导、字体证据、反模板化和质量门禁仍由 docs、core 与执行器承担。

### 哪些旧内容删除，哪些保留

旧图片副本、视觉簇、S01 和未实现的 LoRA 支线已删除；本轮再删除历史排版审计，将逐字变形规范整合到字体手册。活动模块现在按功能命名：`modules/prompt_compiler/`、`layout_engine/`、`scripts/compile_routes.py`、`scripts/create_reference_comparison.py`；编译器测试并入 `tests/`，Schema 和反馈文件名也移除旧版本后缀。

旧路径已移除，使用本 README 的新命令；没有为旧路径新增重复包装脚本。输入中的 `schema_version="0.17"` 是仍兼容的路由数据契约，与 Skill 发布版本独立；不因改目录名而改变字段含义。core 的 version 表示各规则的修订来源。`audit/v019_test_evidence/` 仅保留可追溯的历史测试输入/输出，不属于当前生产协议。

规则入口、解释文档、数值配置、执行代码和测试分别承担不同职责；不为减少文件数而合并成一份难以维护的大文件。最终可读性图像证据保留，防止把历史实验结果误称当前真实生成能力。`.local-history/` 是本机忽略目录，不属于 GitHub 仓库。

### Codex 与 LoRA 的实际边界

当前 Codex 生图工具没有第三方 LoRA 权重、底模或 scale 参数；[OpenAI 图片生成 API 参数](https://developers.openai.com/api/reference/python/resources/images/methods/generate) 也未提供加载外部 LoRA 的接口。下载 `.safetensors`、把触发词写进 Prompt 或声明能力为 true，都不会自动加载权重。

本仓库此前只有 LoRA 元数据检索和兼容/许可检查，没有模型加载器、推理后端、可执行适配器或真实 A/B 证据；所以**当前 Skill 的 LoRA 路径未实现，无法用于这套工作流**。已移除搜索、门禁、Schema、注册表、授权分支及相关测试，正常流程直接采用参考图引导的主视觉生成。

这不代表 Codex 永远无法调 LoRA：另行搭建兼容的外部推理服务并提供可调用 API 后，可以开发新集成；当前仓库不承诺该能力。提示词编译仍不自动调用生图 API，需由 Agent 调用实际可用的生成工具并送入参考图。

## 参考图更新与检索

标签来自文件名，仍待视觉确认。粗检索后必须观察原图，不能直接把关键词得分当作设计匹配证据。

维护命令见 [参考库说明](reference_library/README.md)，浏览 [离线图库](reference_library/previews/gallery.html)。

```bash
python -m pip install -r requirements.txt
python scripts/reference_library.py query --event-type 市集 --typography 手写 --top 12
python scripts/reference_library.py import /path/to/new-posters --collection keyword-YYYYMMDD
python scripts/reference_library.py rebuild
python scripts/reference_library.py previews
```

## 安装与初步校验

参考库工具建议 Python 3.10+（原引擎 Python 3.9+）。需要运行图文可读性模块时，安装 `Pillow`、`NumPy`、`CairoSVG`、`fontTools`；不同操作系统可能需要 CairoSVG 系统图形库。示例 Poster Plan 含测试机的字体绝对路径，应改为本机存在且许可明确的字体文件。

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m unittest discover -s layout_engine/tests -v
python -m unittest discover -s layout_engine/readability -p 'test_readability.py' -v
```

字体集成测试发现本机 Noto CJK/STHeiti 与 DejaVu Sans/Arial；可用 `POSTER_TEST_CJK_FONT`、`POSTER_TEST_CJK_FACE`、`POSTER_TEST_LATIN_FONT` 指定字体。缺字体会明确报错，测试不下载或分发字体。**本仓库目前没有经过独立证明的一键端到端真实生图保证。**

```bash
# 预检活动信息
python scripts/preflight_brief.py examples/brief_complete.json

# 正式项目 JSON 须自行准备，不能直接用 examples 充当生产输入
python scripts/compile_routes.py project.json build/routes

# 先将示例 JSON 的 font_file 修改为本机有效路径
python layout_engine/scripts/build_poster_svg.py layout_engine/examples/example_plan.json build/poster.svg --png build/preview.png

# 对真实 Poster Plan 的成图执行像素可读性审计
python layout_engine/readability/audit_and_repair.py poster_plan.json --out-dir build/readability
```

编译、SVG 预览与最终可读性是不同阶段；**不经 `--visual-review` 且未绑定最终 PNG SHA256 时，只能称候选稿，不是正式通过的交付物**。具体证据流程详见 [可读性模块说明](layout_engine/readability/README.md)。

## 版权与使用边界

参考图库包含来自第三方的视觉素材；入库不意味着已获商业、改编或再分发许可。权属未核实前不得默认商用。仓库未提供统一明确的许可证时，不能推定代码、素材和字体可以自由再分发。旧版文档曾以不同数值解释同一规则，现已合并为当前文档；历史详情通过 [CHANGELOG.md](CHANGELOG.md) 与 Git 提交追溯。

## 专项手册与分支整理

- [参考素材交接格式](collaboration/REFERENCE_BUNDLE_FORMAT.md)
- [最终可读性模块](layout_engine/readability/README.md)
- [最终可读性历史测试证据](audit/READABILITY_AUDIT_V019.md)

两个 refactor 文档分支已由 main 的 PR #1 整合；此次合并记录它们的祖先关系并保留当前已修复的规则，避免恢复过期文件。hygiene 分支已由 PR #3 合并，无须再次合并。分支合并不删除分支，也不重写历史。

## 评审改进与验证

参考 Taste-Skill 的 §0 Brief Inference、§9 反默认套路、§11 先审计后修改、§14 最终预检机制，并将它们适配为海报评审。活动、受众、品牌和 Lead 决定视觉语言；不照搬网页动画、居中/宋体/纯黑禁令或默认配色。机制直接维护在 [质量与交付](docs/QUALITY_AND_DELIVERY.md)，运行此 Skill 不需要 Taste-Skill 依赖。

`core/design_quality_scores.yaml` 是唯一最终评分来源，旧 critic 的 78 分独立门槛已移除。`scripts/poster_review.py` 校验最终 PNG 与缩略图、参考对照/字体/Blueprint/Plan 的材料哈希、逐项预检、语境例外、分项得分与问题复验；Design ≥82、Production ≥85 且所有检查通过才允许正式交付。旧版只填写五段观察的 review 必须迁移到 [新空模板](layout_engine/readability/visual_review_template.json) 并重新看图。

文件完整性与代码回归不能证明评审者真实看图或设计好看，正式项目仍需实际视觉审查。审计保留一组相同输入/输出 JSON（local_uneven），用于证明未发生自动修复；历史可读性证据不得当作当前项目的审批。

团队提供正/负参考与已有概念时，使用 [素材交接格式](collaboration/REFERENCE_BUNDLE_FORMAT.md) 记录学习范围、项目负反馈及权限；概念卡补充素材使用与双语信息空间，详见 [设计与路线](docs/DESIGN_AND_ROUTES.md)。这些是工作流记录，当前脚本不自动解析交接 YAML。

本轮验证：83 项回归测试通过，Skill 入口校验、解析、相对链接与迁移范围比对通过；Markdown 从 19 份减至 17 份，22 个跟踪路径完成迁移。保留路由数据契约 0.17，旧命令与旧视觉审批需按当前文档迁移。
