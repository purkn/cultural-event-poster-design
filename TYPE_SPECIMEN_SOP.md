# H0 中文字体候选样张 SOP

1. 对 Lead 海报进行裁剪：只保留真实海报的 H0/关键字区（不要把转载水印、黑色相册边框裁进去）。
2. 文本采用 brief 中精确的字串；字符 Unicode codepoint + 简/繁选项独立校验。无用户同意不得擅自改变官方名称简/繁或改写字。
3. 候选字体推荐至少 2 款、通常 3 款，每款来自**已授权文件、明确 face index**。绝对不凭字面名称猜测“已安装”。
4. 运行：
   `python scripts/font_coverage.py --font /path/to/font.otf --text '壁上万象' --face <SC_FACE_INDEX> --out /tmp/coverage.json`
   `python scripts/render_type_specimen.py --font /path/to/font.otf --text '壁上万象' --out /tmp/h0-proof.png --face <SC_FACE_INDEX>`
5. 出 1 张多候选比较板：将候选字样与 Lead H0 並置，至少评 width/weight/stroke contrast/terminals/spacing，写差异。
6. 仅把通过的候选进入完整 HTML，明确 `@font-face`。使用 `scripts/type_browser_audit.py` 截图并生成 Font Evidence。
7. 如果 Lead 是定制字体风格而所有候选差异过大：走 `CUSTOM_DISPLAY`，从具备完整 cmap 的合法字形出发做受控字形修改。此时需保存源文本、变形 SVG/PNG、审查报告；不可只输出不可核对的 AI 生中文字。
8. 英文版独立跑一次字体预检与样张，确保不是一个方向过审就直接复制另一个版本。

**禁止通过捷径**：仅用 font-family 字符串作存在性证明；用 `document.fonts.check()` 一项声称字体无 fallback；`font-weight:100` 但字库只有 Regular；用 `transform:scaleX(0.5)` 冒充窄体字；使用系统默认 `serif` 冒充“参考宋体”；使用 CSS 渐变作为字形设计替代。
