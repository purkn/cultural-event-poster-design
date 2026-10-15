# 385张历史参考图检索库

此目录仅保留原图片、哈希、旧P01–P12分桶、接触表及原维护规则，不是当前S1–S8风格分类结果。

- `index.json`：旧桶、图片元数据与近重复/压字经验；`_source_library`指向本目录source_library。
- `source_library/`：385张原图及原源索引；不复制品牌、文字或水印到新活动。
- `previews/`：历史桶接触表，先看缩略再开原图。
- `preset_rules.json`、`overrides.json`：旧分桶规则与历史校正，不是S分类规则。

当前8风格指南见 `../styles/README.md`。从历史图中选候选后按对应S语法实际看图判断，记录本次证据；没有审定就保留NOT_ASSIGNED。旧78条校正仅对旧桶有效，不自动证明新S分类。

维护命令（skill根目录）：

```bash
python scripts/build_style_library.py --verify
```

该脚本只校验/重建**旧检索索引**，不会生成新的S归属。普通海报制作无需重建。新增图须实际看图，避免近重复当不同方案；不因迁移改变已有图像内容或哈希。
