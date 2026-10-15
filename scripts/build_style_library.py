#!/usr/bin/env python3
"""把旧参考库的 385 张图整理成本 skill 的预制风格库。

用法（在本 skill 根目录跑）：
    python scripts/build_style_library.py                # 分桶 + 写 index + 生成接触表
    python scripts/build_style_library.py --no-preview   # 只分桶，不生成图
    python scripts/build_style_library.py --verify       # 校验图片路径与 SHA256 是否还在
    python scripts/build_style_library.py --materialize  # 把图片复制进本 skill，脱离旧库依赖

分桶规则在 libraries/reference_index/preset_rules.json，按数组顺序匹配，命中即停。
要调整风格划分就改那个文件再重跑，不要手改生成的 index.json。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = SKILL_ROOT / "libraries" / "reference_index" / "preset_rules.json"
OVERRIDES_PATH = SKILL_ROOT / "libraries" / "reference_index" / "overrides.json"
INDEX_OUT = SKILL_ROOT / "libraries" / "reference_index" / "index.json"
PREVIEW_DIR = SKILL_ROOT / "libraries" / "reference_index" / "previews"
LOCAL_IMAGES = SKILL_ROOT / "libraries" / "reference_index" / "images"


def load_rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def value_regime(palette: str, rules: dict) -> str:
    """从配色关键词粗分明度家族。只用于预设内部分池，不是风格判据。"""
    vr = rules["value_regime_rules"]
    for p in vr["dark_prefix"]:
        if palette.startswith(p):
            return "dark"
    for p in vr["light_prefix"]:
        if palette.startswith(p):
            return "light"
    for s in vr["light_suffix"]:
        if palette.endswith(s):
            return "mid"
    return "color"


def aspect_class(aspect: float) -> str:
    if aspect is None:
        return "unknown"
    if aspect < 0.62:
        return "long-vertical"      # 长竖版，如 1080x1920 以上
    if aspect < 0.82:
        return "vertical"            # 常规竖版，如 3:4
    if aspect < 1.2:
        return "square"
    return "horizontal"


def assign(rec: dict, presets: list[dict]) -> str:
    """按 preset_rules.json 的顺序匹配标签。match 为 null 的预设只能由 overrides 指进来。"""
    for p in presets:
        m = p.get("match")
        if not m:
            continue
        ok = True
        if "typography" in m and rec.get("typography") not in m["typography"]:
            ok = False
        if ok and "composition" in m and rec.get("composition") not in m["composition"]:
            ok = False
        if ok:
            return p["id"]
    fallback = next((p["id"] for p in presets if p.get("is_fallback")), None)
    return fallback or "P99"


def short_id(full_id: str) -> str:
    return full_id.split(":")[-1]


def apply_overrides(buckets, out_records, overrides, warnings):
    """把视觉校正层叠加到规则分桶结果上。校验 from 是否和规则结果一致，不一致就报警但不阻断。"""
    cur = {rid: rec["preset"] for rid, rec in out_records.items()}
    by_short = {short_id(rid): rid for rid in out_records}
    for short, ov in (overrides.get("reassign") or {}).items():
        rid = by_short.get(short)
        if not rid:
            warnings.append(f"overrides 里的 {short} 在源库中不存在")
            continue
        declared_from, target = ov.get("from"), ov["to"]
        if target not in {r["id"] for r in load_rules()["presets"]}:
            raise ValueError(f"未知目标风格: {target}")
        if declared_from and declared_from != cur[rid]:
            warnings.append(
                f"{short}: overrides 写的是从 {declared_from} 移出，但规则把它分到了 {cur[rid]}；仍按 to={target} 处理"
            )
        buckets[cur[rid]].remove(rid)
        buckets[target].append(rid)
        out_records[rid]["preset"] = target
        out_records[rid]["preset_source"] = "visual_override"
        out_records[rid]["override_reason"] = ov.get("reason")
        out_records[rid]["override_confidence"] = ov.get("confidence", "medium")
        cur[rid] = target

    # 近似重复组必须同桶，否则"生成两版让用户选"会选到同一张图的两个变体
    for g in (overrides.get("near_duplicate_series", {}) or {}).get("groups", []):
        rids = [by_short[s] for s in g["ids"] if s in by_short]
        homes = {cur[r] for r in rids}
        if len(homes) > 1:
            warnings.append(
                f"近似重复组 {g['ids']} 被分到不同预设 {sorted(homes)}（距离 {g.get('distance')}），需在 overrides 里强制同桶"
            )
    return cur


def safe_path(root: Path, relative: str) -> Path:
    result = (root / relative).resolve()
    if Path(relative).is_absolute() or not result.is_relative_to(root.resolve()):
        raise ValueError(f"路径超出参考库: {relative}")
    return result


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_contact_sheets(buckets: dict, presets: list[dict], records: dict, library_root: Path) -> list[str]:
    """每个风格出一张接触表，方便一眼看完整个桶是否视觉一致。"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  ! 没装 Pillow，跳过接触表。pip install pillow 后重跑。", file=sys.stderr)
        return []
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    made = []
    by_id = {p["id"]: p for p in presets}
    for pid in sorted(buckets):
        ids = buckets[pid]
        cols = 6
        rows = (len(ids) + cols - 1) // cols
        tw, th, pad, label = 200, 267, 6, 16
        sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + label + pad) + pad + 24), "#1c1c1c")
        d = ImageDraw.Draw(sheet)
        p = by_id.get(pid, {})
        d.text((pad, 6), f"{pid}  {p.get('name','')}  ({len(ids)} images)", fill="#ffffff")
        for i, rid in enumerate(ids):
            src = safe_path(library_root, records[rid]["image_path"])
            r, c = divmod(i, cols)
            x, y = pad + c * (tw + pad), pad + 24 + r * (th + label + pad)
            if src.exists():
                try:
                    im = Image.open(src).convert("RGB")
                    im.thumbnail((tw, th))
                    sheet.paste(im, (x + (tw - im.width) // 2, y))
                except Exception as e:  # noqa: BLE001
                    d.rectangle([x, y, x + tw, y + th], fill="#440000")
                    d.text((x + 4, y + 4), f"ERR {e}"[:40], fill="#ff8888")
            else:
                d.rectangle([x, y, x + tw, y + th], fill="#333333")
                d.text((x + 4, y + 4), "MISSING", fill="#ff8888")
            d.text((x + 2, y + th + 2), rid.split(":")[-1], fill="#bbbbbb")
        out = PREVIEW_DIR / f"{pid}_{p.get('slug','x')}.jpg"
        sheet.save(out, quality=82)
        made.append(str(out.relative_to(SKILL_ROOT)))
    return made


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-preview", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--materialize", action="store_true")
    args = ap.parse_args()

    rules = load_rules()
    src = rules["source_library"]
    library_root = Path(src["root"]).expanduser()
    if not library_root.is_absolute():
        library_root = SKILL_ROOT / library_root
    library_root = library_root.resolve()
    index_path = safe_path(library_root, src["index"])
    if not index_path.exists():
        print(f"✗ 找不到源参考库索引：{index_path}", file=sys.stderr)
        print("  请恢复源索引或修正 libraries/reference_index/preset_rules.json 中的 source_library；缺少源文件时无法复制。", file=sys.stderr)
        return 2
    src_records = json.loads(index_path.read_text(encoding="utf-8"))
    presets = rules["presets"]
    overrides = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8")) if OVERRIDES_PATH.exists() else {}
    warnings: list[str] = []

    buckets: dict[str, list[str]] = defaultdict(list)
    out_records: dict[str, dict] = {}
    for r in src_records:
        pid = assign(r, presets)
        buckets[pid].append(r["id"])
        out_records[r["id"]] = {
            "preset": pid,
            "preset_source": "rule",
            "substyle": "unassigned",
            "image_path": r["image_path"],
            "sha256": r.get("sha256"),
            "width": r.get("width"),
            "height": r.get("height"),
            "aspect_class": aspect_class(r.get("aspect")),
            "value_regime": value_regime(r.get("palette", ""), rules),
            "event_type": r.get("event_type"),
            "composition": r.get("composition"),
            "typography": r.get("typography"),
            "palette": r.get("palette"),
            "tag_status": r.get("metadata_status", "provisional"),
        }

    apply_overrides(buckets, out_records, overrides, warnings)

    by_short = {short_id(rid): rid for rid in out_records}
    for pid, groups in (overrides.get("substyle_assignments") or {}).items():
        if pid.startswith("_"):
            continue
        for sid, shorts in groups.items():
            for s in shorts:
                rid = by_short.get(s)
                if not rid:
                    warnings.append(f"substyle_assignments 里的 {s} 在源库中不存在")
                    continue
                if out_records[rid]["preset"] != pid:
                    warnings.append(
                        f"{s} 被标为 {pid}/{sid}，但它现在在 {out_records[rid]['preset']}；子风格标注被忽略"
                    )
                    continue
                out_records[rid]["substyle"] = sid

    buckets = {k: sorted(set(v)) for k, v in buckets.items() if v}

    by_id = {p["id"]: p for p in presets}
    sub_defs = {k: v for k, v in (rules.get("substyles") or {}).items() if not k.startswith("_")}
    n_override = sum(1 for r in out_records.values() if r["preset_source"] == "visual_override")
    index = {
        "_generated_by": "scripts/build_style_library.py",
        "_source_library": src["root"],
        "_warning": "生成文件，不要手改。改 libraries/reference_index/preset_rules.json 或 libraries/reference_index/overrides.json 后重跑。",
        "total_images": len(src_records),
        "assigned_by_rule": len(src_records) - n_override,
        "assigned_by_visual_override": n_override,
        "presets": [
            {
                "id": p["id"],
                "slug": p["slug"],
                "name": p["name"],
                "one_liner": p["one_liner"],
                "typical_events": p["typical_events"],
                "note": p.get("note"),
                "count": len(buckets.get(p["id"], [])),
                "substyles": sub_defs.get(p["id"], []),
                "members": buckets.get(p["id"], []),
                "breakdown": {
                    "value_regime": dict(Counter(out_records[i]["value_regime"] for i in buckets.get(p["id"], []))),
                    "aspect_class": dict(Counter(out_records[i]["aspect_class"] for i in buckets.get(p["id"], []))),
                    "event_type": dict(Counter(out_records[i]["event_type"] for i in buckets.get(p["id"], []))),
                    "substyle": dict(Counter(out_records[i]["substyle"] for i in buckets.get(p["id"], []))),
                },
            }
            for p in presets
        ],
        "near_duplicate_series": overrides.get("near_duplicate_series"),
        "text_on_image_evidence": overrides.get("text_on_image_evidence"),
        "records": out_records,
    }

    if args.verify:
        bad_path, bad_hash = [], []
        for rid, rec in out_records.items():
            p = safe_path(library_root, rec["image_path"])
            if not p.exists():
                bad_path.append(rid)
            elif rec["sha256"] and sha256_of(p) != rec["sha256"]:
                bad_hash.append(rid)
        print(f"校验 {len(out_records)} 条：路径缺失 {len(bad_path)}，哈希不符 {len(bad_hash)}")
        for rid in bad_path[:20]:
            print(f"  MISSING {rid}")
        for rid in bad_hash[:20]:
            print(f"  HASH    {rid}")
        return 1 if (bad_path or bad_hash) else 0

    if args.materialize:
        LOCAL_IMAGES.mkdir(parents=True, exist_ok=True)
        copied = 0
        for rid, rec in out_records.items():
            srcp = safe_path(library_root, rec["image_path"])
            if not srcp.exists():
                raise FileNotFoundError(f"源图片缺失: {rid}")
            dst = safe_path(LOCAL_IMAGES, rec["image_path"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            if rec["sha256"] and sha256_of(srcp) != rec["sha256"]:
                raise ValueError(f"源图片哈希不符: {rid}")
            if not dst.exists() or sha256_of(dst) != sha256_of(srcp):
                shutil.copy2(srcp, dst)
            rec["local_path"] = str(dst.relative_to(SKILL_ROOT))
            copied += 1
        (LOCAL_IMAGES / "index.json").write_text(json.dumps(src_records, ensure_ascii=False, indent=1), encoding="utf-8")
        rules["source_library"]["root"] = str(LOCAL_IMAGES.relative_to(SKILL_ROOT))
        rules["source_library"]["index"] = "index.json"
        RULES_PATH.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
        index["_source_library"] = rules["source_library"]["root"]
        library_root = LOCAL_IMAGES
        print(f"已复制 {copied} 张到 {LOCAL_IMAGES.relative_to(SKILL_ROOT)}")

    INDEX_OUT.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n共 {len(src_records)} 张 → {len([p for p in presets if buckets.get(p['id'])])} 个风格预设"
          f"（规则 {index['assigned_by_rule']} / 视觉校正 {index['assigned_by_visual_override']}）\n")
    for p in presets:
        ids = buckets.get(p["id"], [])
        if not ids:
            print(f"  {p['id']:4s} {p['name']:<10s}   0  ← 空桶")
            continue
        vr = Counter(out_records[i]["value_regime"] for i in ids)
        vr_s = " ".join(f"{rules['value_regime_rules']['labels'][k]}:{v}" for k, v in vr.most_common())
        sub = Counter(out_records[i]["substyle"] for i in ids)
        sub_s = f"  子风格已标 {sum(v for k, v in sub.items() if k != 'unassigned')}/{len(ids)}" if sub_defs.get(p["id"]) else ""
        print(f"  {p['id']:4s} {p['name']:<10s} {len(ids):4d} 张   {vr_s}{sub_s}")

    if warnings:
        print(f"\n⚠ {len(warnings)} 条需要留意：")
        for w in warnings:
            print(f"  - {w}")

    if not args.no_preview:
        print("\n生成接触表 …")
        made = build_contact_sheets(buckets, presets, out_records, library_root)
        for m in made:
            print(f"  {m}")
    print(f"\n写入 {INDEX_OUT.relative_to(SKILL_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
