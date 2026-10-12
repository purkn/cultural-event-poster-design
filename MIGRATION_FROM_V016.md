# 安装 / 从 v0.16 迁移

1. **完整替换旧 skill 目录**，不要把 v0.17 解压到已有 v0.16 文件夹里覆盖一部分。旧模块 `modules/prompt_compiler_v016/` 必须不存在，因为它附带的固定“美味发酵节”示例会误导 Agent 复用失败路线。
2. 新的权威入口为 `SKILL.md` 与 `ACTIVE_RULE_INDEX.md`。新编译器：`scripts/compile_routes_v017.py`；参考示例只是测试输入形状，不能直接成为生产值。
3. 对本次发酵节任务，加载 `feedback_registry/fermentation_negative_v017.json`；其他任务不要自动加载它。
4. 生图后必须保存两条不同路线的真实 Rough 和 Lead 对照。用户不喜欢时回到路由阶段，不继续修水印/排版掩盖失败。
5. 外部 LoRA 不支持时 `BASELINE_ONLY` 正常执行；支持时仍保留授权与兼容流程。新版不依赖付费图像 API。
