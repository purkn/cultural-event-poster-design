# LoRA Paired Evaluation & Promotion

## 基准任务
3 个有差异的活动：一个强标题、一个照片/文化素材驱动、一个图形/角色驱动；每个跑 baseline/no-LoRA 与 candidate LoRA，配相同 brief、参考、生成设置和 seed（若后端支持）；至少 2 种 variation/seed。
不允许“换 prompt、换构图、换底模，然后归功于 LoRA”。

## 记录/比较（需要保存并排可视样张）
1. 对 Lead medium/surface/value 的忠实程度
2. 相对于无 LoRA 的风格稳定改善幅度
3. 主体/主题准确性；素材变形能力
4. 构图多样性、避免“所有图都一种样子”
5. H0 文字是否由 glyph-safe/HTML 管理而非假字
6. 技术伪影、额外符号、审美低级化、推理时间/费用

## Promotion
- license/base/size/hash 均已验证；至少 3 briefs × 2 seeds 实测
- 没有参考世界忠实度 Hard RED、没有任务/字体硬失败
- 在至少 2/3 briefs 上相对 baseline 明确胜出；没有一种任务显著退化
- 某个 narrow medium 的收益可以只登记 specific-use，不必称“全风格适用”
- 视觉评估需要并排人工/可靠评审证据；分数只作复核，不得自动给 90+。不满足即 registry `rejected` 或 `experimental`，不得默认调用。

## 否定与可复现
每次保存 `candidate_id`、repo/revision、base model revision、adapter scale、sample params、references、seed、差异评价与审批状态。后端不支持 seed 时说明不可精确复现；不虚报“严格可比”。
