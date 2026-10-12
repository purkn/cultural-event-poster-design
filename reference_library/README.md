# Reference Library v0.13

- `images/REF-XXX.jpg`：规范化参考图
- `index.csv / index.json`：ID、来源、初始 cluster、尺寸与 provisional metadata
- `clusters/*/contact_sheet.jpg`：初始簇接触表
- `coverage.json`：覆盖情况

初始 cluster 只用于检索，不是永久风格分类。

## Strong Lead 限制
带有低置信或 `fallback; needs visual refinement` 元数据的条目，不得仅凭自动标签成为 Strong Lead；必须经过实际视觉检查。

后续可以调整 cluster / tags，但应保持 `REF-XXX` ID 稳定。
