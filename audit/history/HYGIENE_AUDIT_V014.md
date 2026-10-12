# v0.14 hygiene & shortcut review

## Source
Derived from full v0.13 release ZIP, preserving reference library, style pack and original docs. Added small Python scripts that are reviewed in source in this package; they are NOT run automatically.

## Dependency / security design
- `find_lora.py`: only reads Hugging Face public metadata via HTTPS; no model weights downloaded, no arbitrary code execution.
- `preflight_brief.py`: only JSON read and report.
- `lora_gate.py`: only JSON read and report.
- Never automatically load .pkl/.ckpt, run external install scripts, or execute code from model repositories.

## Shortcut regression cases
- Guess a missing date → `WAITING_FOR_USER`.
- Ask for logo despite text signature being possible → forbidden, nonblocking.
- Discover and download LoRA before content confirmed → forbidden.
- Backend unknown but claim LoRA in use → SKIP_NO_BACKEND.
- License unknown but ask user to accept unknown risks → REJECT_UNVERIFIED.
- Model from different base family → REJECT_UNVERIFIED.
- User says yes to one LoRA and agent silently switches model → forbidden.
- LoRA visibly destroys Lead medium/value → fail, return to baseline.
- Evaluate directory structure, call it 'stable high-quality images' → forbidden until actual benchmark.

## Remaining manual gates / honest limitations
The package does not provide an image-generation GPU backend or any LoRA file; no end-to-end LoRA generation has been tested. Visual/style fidelity gates necessarily require rendered-image review. Copyright and redistribution permissions require inspecting each third-party license, not model-card keyword guesses.

## 实际静态审核结果（最终打包前）
- 已运行 10 个 `unittest` 回归测试，全部通过。
- 依赖 PyYAML 解析 59 份 YAML、JSON 解析 23 份 JSON；已校验 143 张 JPEG/PNG 图片。
- 已删除测试产生的 `__pycache__/*.pyc`，不纳入发布包。
- 未实际调用在线 `find_lora` 搜索、下载模型或外部 GPU 推理；这些需目标运行环境测试。
