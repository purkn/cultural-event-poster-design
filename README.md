# 文化活动宣传海报设计 Skill

**v0.20.3 · 参考图驱动 · 多路线主视觉 · 中英双语排版 · 视觉评审与可读性质检**

面向 AI Agent 与设计人员的文化活动海报工作流，适用于展览、市集、演出、文化节与社区活动。以活动简报、用户素材和视觉参考为起点，完成概念探索、主视觉制作、真实字体排版和最终评审，输出可追溯的 SVG、Poster Plan、PNG 与评审材料。

## 设计思路

核心路径是 **活动体验 → 可见概念 → 参考视觉语言 → 海报工艺 → 交付验收**。

1. **从传播目标出发**：明确活动事实、受众、渠道和视觉意图，写出一句 Design Read；让信息量、语气与构图服务于观看场景。
2. **让概念进入画面结构**：概念应改变主体比例、图字关系、阅读路径或空间组织。通过换题测试判断主题专属性，避免依赖一组主题符号表达活动。
3. **用参考建立视觉依据**：选择一张 Lead，拆解构图、媒介表面、字体人格与明度结构，形成 Blueprint；Support 只补一个明确的局部需求。
4. **比较真正不同的路线**：至少两条路线在两个主要视觉维度上产生变化，以实际 Rough 与各自参考并排比较，结合项目反馈选择方向。
5. **用真实字形完成信息层**：核验字体来源、字符覆盖和地区字形，比较标题样张；用同一份 Poster Plan 组织中英文 SVG 与最终合成图。
6. **分别评价设计与生产**：设计评审关注概念、参考忠实度、图字融合和视觉工艺；生产检查关注事实、字符、可读性、输出和素材要求。

```mermaid
flowchart LR
    A[活动简报与素材] --> B[参考检索与概念]
    B --> C[多路线 Rough]
    C --> D[字体与双语 SVG]
    D --> E[最终 PNG 质检]
    E --> F[视觉评审与交付]
    F -->|发现问题| C
```

流程入口见 [SKILL.md](SKILL.md)，规则优先级见 [ACTIVE_RULE_INDEX.md](ACTIVE_RULE_INDEX.md)。

## 参考与评审机制

### 参考图库

图库包含 **385 张不同海报**，按活动、构图、字体和配色四个维度检索。批次 manifest 记录图片身份、尺寸与 SHA256，JSON/CSV 索引及关键词映射由维护脚本生成。105 条编号别名用于定位同一作品；图片身份通过哈希确认。

关键词标签用于粗筛，实际观察原图后才能判断视觉匹配度与 Lead 资格。参考拆解记录“借鉴什么、如何转换、哪些不可照搬”，再用结构、表面、字体和配色对照检查生成结果。

- [离线参考图库](reference_library/previews/gallery.html)：原图浏览与关键词查找。
- [参考库维护说明](reference_library/README.md)：导入、索引、标签与预览。
- [参考系统规范](docs/REFERENCE_SYSTEM.md)：检索、Lead、Blueprint 与忠实度。
- [团队素材交接](collaboration/REFERENCE_BUNDLE_FORMAT.md)：正负参考、学习范围与项目反馈。

### 视觉评审

评审方法参考 Taste-Skill 的 Brief Inference、语境反默认套路、先审计后修改与最终逐项预检。具体应用见 [质量与交付规范](docs/QUALITY_AND_DELIVERY.md)。评审以活动、受众、品牌与参考证据为依据，观察原尺寸终图、25% 缩略图、参考对照和字体证明。

评语应指出具体位置、可见问题和修复动作。反套路检查关注缺乏结构作用的主题符号、装饰性微文案、无参考依据的默认字体/色板以及不必要的效果；有明确语境依据的设计选择可以成立。

正式交付要求 **Design ≥82/100、Production ≥85/100**，逐项预检通过，问题完成修复与复验，并绑定当前 PNG、缩略图、渲染 Plan 及评审材料的哈希。像素质检测量局部对比、背景纹理、主体保护区和缩略信息；审美与语义判断由具备看图能力的评审完成。

## 文件结构与分析

```text
.
├── SKILL.md                         工作流入口
├── ACTIVE_RULE_INDEX.md             规则优先级
├── manifest.json                    版本、模块和图库清单
├── docs/                            简报、参考、设计、字体、质量手册
├── core/                            设计规则、评审清单与量化配置
├── scripts/                         预检、检索、编译、字体与评审工具
├── modules/prompt_compiler/          多路线编译协议及示例
├── layout_engine/                   SVG 排版与像素可读性引擎
│   ├── scripts/                     SVG 构建执行器
│   ├── schemas/                     Poster Plan 数据契约
│   ├── readability/                 合成图质检、评审模板与回归测试
│   ├── examples/                    排版示例
│   └── tests/                       布局回归测试
├── reference_library/               参考图库与检索资源
│   ├── collections/keyword-20261012/ 批次 manifest 与 385 张原图
│   ├── index.json / index.csv        程序索引与人工检查表
│   ├── facets.json / coverage.json  关键词映射与库存统计
│   ├── aliases.json                 编号映射
│   ├── review_queue.json            元数据待复核队列
│   └── previews/                    接触表与离线图库
├── schemas/                         路线与参考证据契约
├── examples/                        简报与 Blueprint 示例
├── feedback_registry/               项目专属负反馈
├── collaboration/                   团队素材交接协议
├── tests/                           工具、规则、字体与评审回归测试
└── audit/                           可读性测试证据
```

结构按 **流程、规则、执行、数据、验证** 划分：

| 层级 | 文件与目录 | 职责与衔接 |
| --- | --- | --- |
| 流程 | SKILL、规则索引、docs | 决定阶段、输入、判断方法与返工位置，按当前任务读取专题手册 |
| 规则 | core | 定义参考、概念、字体及评分约束；最终满分和门槛以 [评分配置](core/design_quality_scores.yaml) 为准，评审清单以 [评审清单](core/universal_poster_critic.yaml) 为准 |
| 执行 | scripts、prompt_compiler、layout_engine | 分别负责输入预检、提示词编译、SVG 构建、像素质检与评审证据验证 |
| 数据 | reference_library、schemas、examples、feedback_registry | 组织图片和检索元数据，约束输入格式，为具体项目提供示例与反馈上下文 |
| 验证 | tests、引擎测试、audit | 验证行为与规则一致性，记录可复核的渲染与测量结果 |

参考库的批次 manifest 是图片元数据来源；派生索引通过脚本重建。`Poster Plan → SVG → PNG → 评审报告` 构成制作和验收链路；字体、参考对照、事实来源与文件哈希提供对应证据。

## 使用与运行

Python **3.10+**。安装项目依赖；CairoSVG 还需可用的系统 Cairo 库。字体文件使用本机存在且许可明确的路径。

```bash
python -m pip install -r requirements.txt

# 活动信息预检
python scripts/preflight_brief.py examples/brief_complete.json

# 按关键词筛选参考
python scripts/reference_library.py query --event-type 市集 --typography 手写 --top 12

# 从正式项目输入编译路线
python scripts/compile_routes.py project.json build/routes

# 构建 SVG 和 PNG 预览
python layout_engine/scripts/build_poster_svg.py poster_plan.json build/poster.svg --png build/preview.png

# 最终合成图质检
python layout_engine/readability/audit_and_repair.py poster_plan.json --out-dir build/readability

# 实际看图、填写评审后验收
python layout_engine/readability/audit_and_repair.py poster_plan.json --out-dir build/readability --visual-review review.json
```

生图阶段由 Agent 调用实际可用的生成/编辑工具并提交参考图片，提示词编译器负责组织输入。正式项目 JSON 应在项目目录准备；示例中的活动、字体与视觉观察需按实际任务填写。

评审从 [空模板](layout_engine/readability/visual_review_template.json) 开始，按 [可读性模块说明](layout_engine/readability/README.md) 填写材料路径、哈希、分项分数、检查与问题复验。

### 图库维护

```bash
python scripts/reference_library.py import /path/to/posters --collection keyword-YYYYMMDD
python scripts/reference_library.py rebuild
python scripts/reference_library.py previews
```

### 回归验证

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s layout_engine/tests -v
python -m unittest discover -s layout_engine/readability -p 'test_readability.py' -v
```

渲染与测量案例见 [可读性测试证据](audit/READABILITY_AUDIT_V019.md)。

测试字体可通过 `POSTER_TEST_CJK_FONT`、`POSTER_TEST_CJK_FACE`、`POSTER_TEST_LATIN_FONT` 指定。文件完整性和自动测试验证技术行为，正式视觉验收仍需要真实看图。

## 专题手册

- [简报与素材](docs/BRIEF_AND_ASSETS.md)：活动事实、来源、素材授权与双语信息。
- [设计与路线](docs/DESIGN_AND_ROUTES.md)：Concept、素材使用、路线差异与项目反馈。
- [字体系统](docs/TYPOGRAPHY_SYSTEM.md)：字体人格、字形证明与图字工艺。
- [SVG 排版](layout_engine/SVG_FIRST_LAYOUT.md)：母版、文字层与布局执行。
- [质量与交付](docs/QUALITY_AND_DELIVERY.md)：评分、预检、修复闭环与证据协议。

## 素材与使用范围

第三方参考图的入库不代表已获得商业、改编或再分发许可。正式项目需核实图片、字体、品牌与人物素材的使用范围；仓库的代码与素材许可按实际授权文件确认。
