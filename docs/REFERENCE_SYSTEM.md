# 参考图检索与视觉保真规范（v0.19）

## 适用与权威来源
本文件统一参考图选取、Lead/Support 边界、拆解、色彩/媒介验证。可执行数值优先取自 `core/lead_validity_gate.yaml`、`core/reference_deconstruction.yaml`、`core/reference_blueprint_contract.yaml`、`core/reference_delta_gate.yaml` 等配置；本页描述业务语义，若文字与配置不同，先停止并以配置核实。强参考不意味着模仿原作者具体图形、品牌字形、角色或 Logo。

## 两阶段检索
按参考索引粗检索约 16 张，再对约 8 张候选进行真实视觉观察与精拆，禁止仅凭文件名、风格词或自动标签宣布符合。视觉比对必须记录不确定项。参考库十个簇属于暂定分类，不等于十个已验收 Style Pack。

## Lead 判定
检查空间结构、媒介/表面、字体 DNA、色彩/明度四维；仅布局相似时标记 `STRUCTURE_ONLY_REFERENCE`，不可称 Strong Lead。
阈值由 `core/lead_validity_gate.yaml` 维护：topology≥0.70、medium_surface≥0.65、typography_DNA≥0.60、palette_value_regime≥0.60、overall≥0.68；至少三类达到 MEDIUM。若预期需突破两个及以上全局维度，重新选择 Lead。

## 拆解与蓝图
明确记录：
- STRUCTURE：H0/主视觉/信息区边界框和面积比例、主轴、视觉中心、图文关系、密度与留白；
- SURFACE：媒介、平面/立体程度、边缘、光照、纹理、表面质感、背景明度；
- TYPE DNA：骨架、笔画对比、字重/字宽、比例、排列、填充、效果、正文/英文/数字角色；
- PALETTE：背景/主色/辅色/强调色及明度、饱和度、面积占比与来源；
- BORROW / TRANSFORM / DO NOT COPY：分别标记保留、内容转译、禁止复刻的元素。
不要把估计面积说成像素级实测。参考拆解 rerank 权重只采用 `core/reference_deconstruction.yaml`，不要重用旧 v0.13 文档中求和为 75 的权重。

## Lead 与 Support
Lead 主导拓扑、媒介、色彩结构、标题人格和负形组织。Support 最多填补一个明确的局部变量，需在开始前填写 `support_scope`，不得借 Support 改写整张图的视觉世界。
Strong Lead 的构图面积容差、视觉中心偏移和色彩角色容差以 `core/reference_blueprint_contract.yaml` 为唯一数值来源，不能在生成后才解释超界。

## 偏差门禁
必须在实际生成图与 Lead 并排观察下分别填写 Structure Delta、Surface Delta、Typography Delta。
背景 high-key ↔ low-key 反转，二维版画变为 3D/发光流体，无依据的平面 H0 变多色发光、主体图字关系改变等均为 RED；RED 不允许靠主题解释或自评总分覆盖，返回重新路由。
颜色从 Lead → Style Pack → Concept → 活动语义依次取证，禁止“科技自动蓝紫、传统自动红金、儿童自动彩虹”。具体状态与硬失败定义见 `core/palette_structure_gate.yaml`、`core/medium_surface_fidelity_gate.yaml`、`core/reference_delta_gate.yaml`。
