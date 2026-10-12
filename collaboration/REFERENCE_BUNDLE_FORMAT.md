# 参考图 ZIP 格式 v0.13

## A. 最省事：未分类 ZIP（允许）
用户可以直接给一个装满参考图的 zip。系统负责 provisional clustering；不要求提前分风格。

## B. 团队开发 Style Pack 时推荐结构
```text
MyStyle_reference_bundle.zip
  manifest.yaml
  positive/
  negative/
  notes/README.md   # 可选
```

manifest 可写：
```yaml
provisional_style_name: optional
positive_refs:
  - file: positive/01.jpg
    learn: [hero, artword, topology]
    do_not_learn: [specific_subject]
negative_refs:
  - file: negative/01.jpg
    avoid: [safe_template, weak_H0]
```

注意：备注只是人工提示，视觉检查仍优先。
