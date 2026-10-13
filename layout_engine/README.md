# SVG 排版与可读性引擎

这个目录是文化活动海报 Skill 的当前排版引擎。它不是“SVG 比 HTML 天然高级”的宣称，而是把**固定尺寸图形化编排**交给 SVG，把信息母本保存在 JSON 中。

- `SVG_FIRST_LAYOUT.md`：使用范围、SVG/HTML 双路线与交付规范
- [字体规范](../docs/TYPOGRAPHY_SYSTEM.md)：包含逐字变形条件及真实字形证据
- `scripts/build_poster_svg.py`：文字仍为可修改 SVG 文本节点的执行器
- `tests/test_svg_layout.py`：越界、字体、默认禁令、组合错误测试
- `schemas/poster_plan.schema.json`：输入配置契约

需要 Python + Pillow，PNG 可选 cairosvg。字体文件只作为本机验证路径使用，本包**不附带第三方字体文件**。

示例 JSON 中的字体路径为本次测试环境的路径，换一台机器时请替换成已有且获授权的字体文件。`font_family` 应与文件中真实字体保持一致；两者未核对时不得报审美验收 PASS。

示例命令：
```bash
python layout_engine/scripts/build_poster_svg.py layout_engine/examples/example_plan.json /tmp/poster.svg --png /tmp/poster.png
python -m unittest discover -s layout_engine/tests -v
```


## 最终出图必走 Readability Gate
此目录新增 `readability/audit_and_repair.py` + `readability/README.md` + 合成图回归测试；原 `build_poster_svg.py` 直接导出只能作为**结构预览**，不具备成图可读性 PASS 权限。运行：

```bash
python layout_engine/readability/audit_and_repair.py plan.json --out-dir build/readability
# 查阅报告与 final_render.png，由视觉 Agent 完成标注、SHA256 绑定复核
python layout_engine/readability/audit_and_repair.py plan.json --out-dir build/readability --visual-review build/readability/review.json
```
无需付费模型：此模块用本地 CairoSVG / Pillow / NumPy / fontTools；需要有能实际查看最终渲染图片的 Agent 完成最后审美和语义主体检查。
