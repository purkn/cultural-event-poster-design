# 六目录真实交付

各语言分层共用同画布、像素尺寸、坐标及色彩约定。用户要求的语言各自有成品及对应层，可共享同一主视觉但不要伪造不同图像。仅输出请求的格式，PNG为默认图像交付；PDF需按实际输出工具生成并验证，不能把改扩展名当PDF。

```
poster_project/
  01_final/poster_zh.png           # 正式版，另有请求的语言与预览
  02_hero/hero_zh.png              # 无正式文字主视觉，全画布
  03_title/title_zh.png            # 透明H0，全画布；真实可编辑时另附SVG
  04_text/text_zh.png              # 透明正文，全画布；另交真实文本排版源
  05_source/layers_zh.svg          # 合成工程及实际素材；如为栅格层须如实标注
  05_source/text_zh.svg            # 正文真实可编辑文字节点，制作时保留
  06_metadata/
    activity.json                 # fields:{theme,languages,purpose,output_dimensions,...}，每项value/status/source
    activity_profile.json         # 五维标签、证据与置信度
    design_plan.json               # S主风格/局部辅助、M主骨架、独立参数、V/H空间模式、区域蓝图、主体保护区、判定证据、概念、标题、语言、参考、实际生成参数
    workflow_state.json            # input/style/visual/feedback四处交互记录，schema_version=1，详见checkpoints.md
    readability_zh.json            # 真实检测报告
    quality_zh.json                # 四硬项、两美学项及核验观察
    composition_zh.json            # 图层尺寸、模式、是否可编辑等事实
    text_combined_zh.png           # 完整文字透明层，给字形采样
    feedback.json                 # 当前项目反馈，未答复不记accepted
```

`compose_layers.py`只组装真实三层并生成包含嵌入PNG的SVG工程，不会自动生成正文的可编辑文本。该工程可移动/隐藏栅格层，不是完全矢量排版。真正的可编辑正文SVG `05_source/text_<语言>.svg` 需在制作时保留文字节点和字体信息；正式检查会拒绝只有嵌入图片的正文源；图像H0是位图，要改字需重生成，不把嵌入PNG称可编辑字形。

质量记录 `quality_<语言>.json` 结构：`hard_gates` 下text_accuracy/readability/layer_integrity/content_completeness各为 `{status, evidence}`；`aesthetics` 下design_quality/style_consistency各为 `{score:1..5, evidence, issues}`；`design_review` 下 `{verdict, evidence}`。证据为真实观察、预览/报告位置，不是空的自我打分。每种语言分别核字、缩略可读性与断行。

正式交付前：三层精确叠合等于成品；透明层有透明区域且非空；像素/坐标正确；P0与适用P1已提供、推断经确认或授权虚构，未决项只能作预览；所提供Logo/二维码/署名没有遗漏；真实文字与简报一致，二维码有实际来源且扫出正确链接；硬门禁均PASS，设计复核PASS。非适用字段注明理由，不能伪造二维码。

无文字背景、精确图层或核验能力缺失时，明确交“预览/合成设计稿”和缺项，不宣称完整分层或正式门禁通过。仅换语言文字不应把原主视觉重生成至风格漂移。

同活动迭代建新版本目录，脚本不覆盖旧成品。真实文件清单随交付附上，不提前将计划写成已生成结果。
