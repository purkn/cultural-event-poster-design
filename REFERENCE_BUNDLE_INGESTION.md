# Reference Bundle Ingestion v0.13

## 原则
用户可以直接提交未分类 ZIP，不要求预先做好风格分类。

## 自动处理
1. 解包并过滤 `.DS_Store` / `__MACOSX` 等噪音。
2. 给每张图分配稳定 `REF-XXX` ID。
3. 记录原文件名与来源目录。
4. 进行 provisional visual clustering。
5. 标记 topology / asset structure / type-image relation / material / information density。
6. 生成 coverage map。
7. 只有成熟 cluster 才晋升 Style Pack。

## 关键卫生规则
- 文件名与目录名只是提示，不是视觉分类真理。
- 自动 cluster 只用于检索，不可直接当 Style Pack。
- `fallback; needs visual refinement` 等低置信元数据不得触发 Strong Lead。
- 新 ZIP 合入后保持既有 REF ID 稳定。

当前 Library：113 张静态参考；cluster 状态仍为 provisional。


## Lazy Deconstruction（v0.13）
新 ZIP 导入时不要求人工把每张图完整分类。
导入阶段只做：
- 文件规范化
- 粗粒度视觉簇
- 质量/可读性/重复项判断
- provisional tags

真正的结构精拆在检索 Top 6–8 时按需执行。这样参考库可以持续扩容，而不需要先穷举分类。
