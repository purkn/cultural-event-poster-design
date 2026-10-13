# 团队参考素材交接

未分类图片目录也可提交，不要求先建风格分类。入库沿用 [参考库维护说明](../reference_library/README.md) 的批次命名空间、SHA256 和别名机制；整理文件名为 `REF-NNN_活动_构图_字体_配色`。未确认标签写“未知”，不根据文件名猜测视觉结论。当前导入脚本接收图片目录，ZIP 需先安全解包、过滤系统元数据，不能把自动解包当作已实现能力。

## 带说明的团队交接（可选）

可保留 `positive/`、`negative/` 与 `notes/`，并提供如下人工说明：

```yaml
project_id: event-project-id
positive_refs:
  - file: positive/01.jpg
    learn: [topology, type_image_relation]
    do_not_learn: [specific_subject, original_wording]
negative_refs:
  - file: negative/01.jpg
    avoid: [weak_H0, generic_sticker_sheet]
    reason: 标题与主视觉相互独立，缺少结构关系
```

此 YAML 是团队交接记录，当前工具不自动解析。为图片整理关键词名称后再导入；这不会自动把 `positive/negative` 变成图片等级，也不会创建旧式 Style Pack。负参考默认只约束 `project_id` 对应项目；确有跨项目通用问题时，需要明确说明范围与证据。备注是待核提示，真实图片观察优先。

每次交接还需记录原文件名/来源、素材权利与允许修改范围、已观察与尚未观察的图片、已有候选路线和否定理由，以及 Rough/字体样张/最终 PNG 的证据位置。明确哪些是原作者不能复制的独有内容；不把收集或转交当作授权。

## 按需精拆与接收

导入阶段只做文件、哈希、尺寸、重复项和 provisional 标签检查，随后对检索选中的候选按 [参考系统](../docs/REFERENCE_SYSTEM.md) 精拆；不要求全库逐张完成 Blueprint 才能使用。看图后记录空间拓扑、媒介、H0 DNA 与信息密度，不用旧簇成熟度或备注直接晋升 Strong Lead。

接收时先核对活动事实和素材权限，再检查路线与参考的关系、H0 策略、媒介/配色漂移、负空间和双语信息承载。按当前 [质量门禁](../docs/QUALITY_AND_DELIVERY.md) 验收；交接说明、编译成功与技术可读性 PASS 均不能代替真实视觉审批。
