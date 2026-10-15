# 四处用户交互与项目状态

依次为资料核对 → 风格确认 → 主视觉 A/B 选择 → 交付后用户评价与自我升级。

## 资料核对（input）
无论资料是否齐全，先展示活动事实、语言、用途、尺寸与待定项，集中请求确认。用户本轮已明确确认同一份资料可直接记录，不重复问。已授权虚构的信息标明 fictional；缺失、不适用和待定分开。虚构授权不等于豁免其他断点。

## 风格确认（style）
展示1主方案、2–3替代，说明主辅职责、两条适配依据、一条代价及可行构图。真实参考先看图，无已核验参考就明说文字指南驱动。收到选择才开始生图；用户已明确指定可记录为确认。

## 主视觉 A/B 选择（visual）
先做准确标题的粗排骨架，再分别规划两个概念。生成两张无正式文字主视觉，同时展示标明“排版示意”的标题位置/尺度预览；它不是正式H0。两概念至少在母题、空间组织、图字关系中两项不同。收到选择才做正式艺术字、正文和分层。S4以文字骨架主导构图，不能先做任意背景再硬塞标题。

## 用户评价与自我升级（feedback）
先交真实文件，再询问满意度与问题分类。未回复保持 feedback_review，不扣留成品、不假定满意。反馈定位模块→局部修改→前后复评→案例记录。核心升级仅在多案例验证、回归和明确授权后发生；未满足时记录候选改进，不宣称已自我升级。

## 执行与恢复
项目状态只存 `06_metadata/workflow_state.json`。使用 `scripts/workflow_state.py` 初始化、记录实际原话/选择、检查和恢复。`build_style_prompt.py --state ...` 拒绝未完成前置确认的制作提示词。脚本不能证明原话确实来自用户，也不能拦截绕过脚本的直接工具调用；助手仍须遵守流程。

示例（路径均属当前项目）：
```bash
python scripts/workflow_state.py --state project/06_metadata/workflow_state.json init
python scripts/workflow_state.py --state project/06_metadata/workflow_state.json decide --checkpoint input --quote '用户实际确认原话'
python scripts/workflow_state.py --state project/06_metadata/workflow_state.json decide --checkpoint style --selection S1 --quote '用户实际选择原话'
python scripts/build_style_prompt.py --state project/06_metadata/workflow_state.json --style S1 --stage hero_a --values values.json
```

资料/风格/候选变化时 `reopen --checkpoint input|style|visual --reason ...`，失效该点及后续确认，保留历史与新修订号。交付前还须通过 validate_output.py 和人工质量复核；`deliver --quote '实际文件路径与评审证据'`只记录实际交付，不运行质量审查。交付后按feedback/rules.md收集评价，再decide反馈。旧交付记录不能批准新一轮制作。

每个项目独立记录，批量可以合并提问但逐项保存回答。仅明确授权可按项目范围豁免对应确认；无回复、超时、预选、数量要求、虚构授权均不算。发问后停止该分支依赖工作并结束本轮，工具accepted不等于批准。
