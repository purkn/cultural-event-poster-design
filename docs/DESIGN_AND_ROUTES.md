# 创意路线、视觉设计与反馈规范（v0.19）

## 设计决策顺序
先理解活动体验和创意机制，再从实际参考图推导视觉世界；创意改变画面结构，不是解释已经生成的物件。构图、媒介、颜色、字形和图文关系共同决定路线。制作至少两条真正不同的 `{lead, concept, palette, typography, layout}` 路线，而非同色方案换细节；Prompt 编译器以 `modules/prompt_compiler_v017/PROMPT_COMPILER_V017.md` 为接口契约。

## 反通用模板
- 装饰必须源自 Lead、承担 Concept 的结构作用、保留用户指定素材或得到 Style Pack anchor 证据；无必要散点图标默认删去。
- 自然/音乐/科技/儿童/传统等题材，不默认附加太阳音符、星星、蓝紫发光、红金印章或随机渐变。
- 留白需满足功能或视觉张力：被关键元素围合、形成视线通道、继承参考的负形、承载信息或形成尺度对比中的至少两项；纯粹空缺不计分。
- 渐变、发光、玻璃、阴影、立体效果不是“主题化”的默认工具；仅在 Lead 或结构概念确有依据时采用。
详见 `core/semantic_decoration_ban.yaml`、`core/negative_space_gate.yaml`、`core/h0_strategy_router.yaml`。

## 反馈优先
用户否定配色、字体或美感时，原先 Design PASS 不能抵消。只将拒绝约束作用于对应项目，记录 `route_fingerprint`、被否定维度与 `must_change`；新路线必须更改相应设计机制，不能只换少量图标、日期或底色。现有 `feedback_registry/fermentation_negative_v017.json` 只适用于对应历史项目，不能成为所有活动的全球黑名单。

## 验证顺序与防偷懒
首先检查活动信息是否确认，实际观察 Lead，再编译 prompt 和生成 hero rough；观察【Lead／Prompt／实际生成图】并排证据，审查配色明度、标题人格、构图、主体表现和相似性；早期失败应重选路线，而不是先做字体、排版和美化。若后端未实际接收图像参考，明确写 `TEXT_ONLY_REFERENCE_FALLBACK`。没有真实出图不得判设计 PASS。
设计评分与生产评分相互独立；具体门禁与唯一评分表见 `QA_ACCEPTANCE.md`、`core/design_quality_scores.yaml`；图文可读性另由 `layout_engine_v018/readability/README.md` 的实际渲染检查控制。
