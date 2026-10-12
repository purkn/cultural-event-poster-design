# Brief Intake & Breakpoints — v0.14

## 前置事实等级
所有结构化字段包括 `{value, status, source, official}`；status 为 confirmed / draft / missing，source 为 user_pdf、user_text、user_asset、official_source 或 inference。
**inference 不得伪装 confirmed**。从演示海报中“看起来合理”的日期、场地、费用不得填入真实 brief。

### P0 Hard blockers（正式活动海报）
- `title`: 活动正式中文名称；输出英文正式名称如不存在，可先草译，但当用户要求“官方英文全称”时必问。
- `date_start` 或 `date_text`: 日期（若为单日活动）；时间未给且被要求必须呈现时须问。
- `venue_name` 或准确的线上 `online_url`：按实体 / online / hybrid 判定。
- `registration_link`：当用户明确要求二维码、可点击报名链接时才 P0。
- `ticket_price`: 当 brief 明确说明海报必须展示票价但价格未提供时才 P0。
- 主办方确认：当用户要求展示官方主办身份但资料来源未给时 P0；否则可省略署名。

### P1 Confirmation before final
- 英文专有名称缺官方译名：允许生成 draft 版式测试，但正式定稿需确认或使用用户认可的中性译法。
- 多个日期、不同场次时间、多个校区/场馆冲突：先确认，不做“推测最可能”。
- 活动二维码只给了报名网站文字：需确认 QR 的落点（不能自造网址）。
- 素材有不可修改的版权/肖像/文物条件：不清晰时请求授权范围。

### P2 Nonblocking
- 未提供 logo → 推荐文字主办方署名；不要造 logo。
- 未提供视觉图 → AI 生成 Hero；若用户明确指定“必须使用提供的素材”而素材缺失，则询问。
- 未给受众 → 可从活动类型形成有标记的工作假设。
- 没给 tagline → 如非官方指定，可提出原创候选、不要伪装为官方用语。
- 未指定比例 → 推荐 4:5 竖版；不要说是用户要求。

## 必问断点：BP_CONTENT
发生在任何生图、LoRA 查找、字体下载之前。一次只问真正阻止工作的关键信息，多个独立缺口可合并成一条简短问题：
> 我建议先按 4:5 竖版、中英双版继续。当前正式名称已确认，但缺活动日期与准确地点。请提供这两项；如果这是预热海报，也可以明确允许标注“日期／地点待公布”。

## BP_CONFLICT
例如 PDF 11/08 与聊天文本 11/18 不一致 → 引述两个来源并询问采用哪一项；不得擅自挑选。

## BP_ASSET_RIGHTS
素材需明显变形、保留身份或涉及权利声明不清时，询问可用范围；对用户提供的普通设计原料默认 ADAPT 但不超出其明确限制。

## BP_LORA_DOWNLOAD（必须和 BP_FONT_DOWNLOAD 分开）
当兼容+权限齐全的候选明确胜过基线测试需求且未缓存才触发：
> 我推荐 LoRA「[名称]」，来自 [托管方/作者链接]，适配 [底模版本]，约 [MB]，许可证 [精确名称及用途许可]；预计保存到项目缓存，[是否有模型或网络费用]。这是可选增强，拒绝后仍可使用普通生图。是否授权下载并用于本次测试？

如 license/大小/作者/底模未知，**不得触发“同意下载吗”作为跳过查证的捷径**，应改为不用该候选。

## BP_FONT_DOWNLOAD
单独解释选择逻辑、字体授权/来源/大小，仅在安装字体确有必要时询问。

## 内部状态
NEEDS_INFO / READY_BASELINE / READY_LORA_DISCOVERY / WAITING_FOR_LORA_APPROVAL / READY_TO_RENDER / QC_FAILED / DONE。
所有需用户决策的断点停止当前执行，收到答复后恢复；不要自动承诺后台持续处理。

## v0.15 BP_FONT_DOWNLOAD 补充
中文/英文实际标题字体文件无匹配候选时，按 `docs/TYPOGRAPHY_SYSTEM.md` 给出最优推荐与权限证据，不得默默回退。下载或授权请求不能被 LoRA 许可替代。
