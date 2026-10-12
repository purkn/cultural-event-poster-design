# 参考图库 v0.19.1

401 张不同海报；514 条索引记录含原 113 条历史编号。新批次包含原库全部图片，检索按 SHA256 去重。桌面源文件保持原样。

## 文件结构

```text
reference_library/
  collections/
    keyword-20261012/
      manifest.json          新批次权威元数据与哈希
      images/                保留关键词文件名的 401 张原图
    legacy-v013/
      manifest.json          旧 113 个 ID 与原图路径
      coverage-v013.json     旧视觉簇统计快照
  images/REF-XXX.jpg          旧路径保留，供历史案例使用
  clusters/                  旧 provisional 视觉簇及接触表
  index.json / index.csv     从批次 manifest 生成的统一索引
  facets.json                活动 / 构图 / 字体 / 配色 → ID 列表
  aliases.json               重复图片 ID → canonical ID
  review_queue.json          含未知标签的待检查 ID
  coverage.json              总量、去重、批次、标签、未知项统计
  previews/                  每页 40 张接触表、页清单、离线图库
```

旧 `REF-001` 与新 `keyword-20261012:REF-001` 是不同编号；不得根据尾部序号推断对应关系。真正对应关系由图片哈希确定。`image_path` 相对于本目录，`source_path` 仅记录来源，不是运行时路径。新批次名称记录采集批次，不是每次维护日期。

## 更新与检索

Python 3.10+，依赖 `pip install -r requirements.txt`。在项目根目录运行：

```bash
python scripts/reference_library.py import /path/to/new-posters --collection keyword-YYYYMMDD
python scripts/reference_library.py rebuild
python scripts/reference_library.py previews
python scripts/reference_library.py query --event-type 艺术展览 --composition 非对称网格 --typography 无衬线 --palette 蓝 --top 12
```

导入名为 `REF-NNN_活动_构图_字体_配色.jpg`，支持 jpg/jpeg/png/webp。同批次重复执行不会增加记录或覆盖视觉注释；同 ID 不同图片会拒绝，应使用新批次。重新标注时修改批次 `manifest.json`，再 rebuild 和 previews；生成的 index/facets 不应手工维护。原图哈希与尺寸校验失败会阻止重建。

查询采用各字段的子串匹配、命中项加权排序：构图 4、字体 3、配色 2、活动 1；不要求全部字段同时匹配，返回 `matched_fields` 便于检查。去除重复图片后取 Top K。无命中时浏览旧视觉簇或离线图库，再进行视觉检索。

## 视觉证据边界

四维标签来自文件名，状态为 provisional；16 张含未知标签。数量覆盖不代表媒介、字形或风格成熟度。关键词得分不等于细粒度匹配分，不能直接晋升 Strong Lead 或 Style Pack。实际观察 Top 6–8 原图，按照 `docs/REFERENCE_SYSTEM.md` 与 Lead/Blueprint 门禁精拆，再决定用途。旧簇可继续辅助检索，历史覆盖判断不能套用整个新库。

## Git 维护

更新前 `git pull --ff-only`；导入、重建、预览后检查 `git diff --stat`，执行测试，再 `git add`、`git commit`、`git push`。不强制推送；若远端已有新提交，先合并并复检。
