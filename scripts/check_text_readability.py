#!/usr/bin/env python3
"""叠字可读性检查。只依赖两张 PNG 和一份文字块清单，不绑定任何排版引擎。

为什么需要它：中文海报最高频的翻车是文字压在图上看不清。生成模型和人都容易
自我感觉良好，所以这一步必须用像素说话，且不允许用别的分数补偿。

输入：
  --final      最终成品 PNG（含文字）
  --background 同一画面去掉文字后的 PNG（生图时保留一份无字底图）
  --blocks     JSON：[{"id":"h0","bbox":[x,y,w,h],"color":"#FFFFFF","font_px":96,"role":"h0"}]
               role 取 h0 / key / body，阈值不同
  --text-layer 可选：同尺寸透明 RGBA 全文字层（含文字效果），按实际字形采样
  --scale      缩略比例，默认 0.25（模拟手机列表里的尺寸）

输出：每块 PASS/FAIL 与原因，整体 gate=PASS/FAIL。退出码 0=通过。

它测三件事：
  1 对比度：文字色与块内背景逐像素的 WCAG 对比度，传入透明文字层时只采样字形覆盖的像素
  2 背景噪声：块内背景的边缘密度和明度方差，仅作为复核提示，不能把纹理直接等同于不可读
  3 缩略字号：按 --scale 缩放后字号是否还够大

它不测审美，也测不了主体遮挡——那部分必须人眼看最终图。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

THRESH = {
    # contrast: WCAG 对比度下限；pass_fraction: 块内达标像素占比下限
    # edge_density / luma_std: 背景噪声上限；min_thumb_px: 缩略后字号下限
    "h0":   {"contrast": 3.0, "pass_fraction": 0.90, "edge_density": 0.20, "luma_std": 0.22, "min_thumb_px": 12.0},
    "key":  {"contrast": 4.5, "pass_fraction": 0.92, "edge_density": 0.18, "luma_std": 0.205, "min_thumb_px": 7.5},
    "body": {"contrast": 4.5, "pass_fraction": 0.92, "edge_density": 0.15, "luma_std": 0.18, "min_thumb_px": 6.0},
}


def srgb_to_lin(rgb: np.ndarray) -> np.ndarray:
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def luminance(rgb: np.ndarray) -> np.ndarray:
    lin = srgb_to_lin(rgb)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def wcag(l1: np.ndarray, l2: np.ndarray) -> np.ndarray:
    hi, lo = np.maximum(l1, l2), np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def parse_color(c: str) -> np.ndarray:
    if not isinstance(c, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", c):
        raise ValueError("color 必须是 #RRGGBB")
    c = c[1:]
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255.0


def edge_density(luma: np.ndarray) -> float:
    gx = np.abs(np.diff(luma, axis=1))
    gy = np.abs(np.diff(luma, axis=0))
    g = np.zeros_like(luma)
    g[:, :-1] += gx
    g[:-1, :] += gy
    return float((g > 0.12).mean())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", required=True)
    ap.add_argument("--background", required=True)
    ap.add_argument("--blocks", required=True)
    ap.add_argument("--text-layer", default=None)
    ap.add_argument("--scale", type=float, default=0.25)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if not math.isfinite(args.scale) or not 0 < args.scale <= 1:
        raise ValueError("scale 必须在 (0,1] 内")
    bg = Image.open(args.background)
    fin_source = Image.open(args.final)
    for im in (bg, fin_source):
        if "A" in im.getbands() and im.getchannel("A").getextrema()[0] < 255:
            raise ValueError("输入底图和成品必须不透明，请先按真实底色合成")
    bg = bg.convert("RGB")
    fin = fin_source.convert("RGB")
    fin_arr = np.asarray(fin)
    if bg.size != fin.size:
        print(f"✗ 底图和成品尺寸不一致：{bg.size} vs {fin.size}", file=sys.stderr)
        return 2
    bg_pixels = np.asarray(bg)
    text_pixels = None
    if args.text_layer:
        text_image = Image.open(args.text_layer)
        if text_image.size != bg.size or "A" not in text_image.getbands():
            raise ValueError("文字层必须是同尺寸且带 alpha 的透明图像")
        text_pixels = np.asarray(text_image.convert("RGBA"))
        if np.all(text_pixels[..., 3] == 255):
            raise ValueError("文字层必须有透明区域，不能用不透明底板冒充字形")
    bg_arr = bg_pixels.astype(np.float64) / 255.0
    blocks = json.loads(Path(args.blocks).read_text(encoding="utf-8"))

    if not isinstance(blocks, list) or not blocks:
        raise ValueError("blocks 必须是非空列表")
    seen = set()
    for b in blocks:
        if not isinstance(b, dict) or not isinstance(b.get("id"), str) or not b["id"] or b["id"] in seen:
            raise ValueError("文字块 id 必须非空且唯一")
        seen.add(b["id"])
        box = b.get("bbox")
        if not isinstance(box, list) or len(box) != 4 or any(type(v) is not int for v in box):
            raise ValueError("bbox 必须是四个整数")
        fp = b.get("font_px")
        if type(fp) not in (int, float) or not math.isfinite(fp) or fp <= 0:
            raise ValueError("font_px 必须是正有限数")
        parse_color(b.get("color"))
    results, gate_fail = [], False
    for b in blocks:
        role = b.get("role", "body")
        t = THRESH.get(role)
        if t is None:
            print(f"✗ 未知 role {role}（可选 h0/key/body）", file=sys.stderr)
            return 2
        x, y, w, h = (int(v) for v in b["bbox"])
        if x < 0 or y < 0 or w <= 2 or h <= 2 or x + w > bg.width or y + h > bg.height:
            results.append({"id": b["id"], "verdict": "FAIL", "reasons": ["bbox 越界或为空"]})
            gate_fail = True
            continue
        patch = bg_arr[y:y + h, x:x + w]
        luma_bg = luminance(patch)
        support = np.ones((h, w), dtype=bool)
        composition_ok = True
        if text_pixels is not None:
            tp = text_pixels[y:y + h, x:x + w]
            alpha = tp[..., 3].astype(np.float64) / 255.0
            support = alpha >= 0.9
            if not support.any():
                support = alpha >= 0.5
            if not support.any():
                results.append({"id": b["id"], "verdict": "FAIL", "reasons": ["文字层在该块内没有足够可见的字形像素"]})
                gate_fail = True
                continue
            expected = tp[..., :3].astype(np.float64) * alpha[..., None] + bg_pixels[y:y+h, x:x+w] * (1-alpha[..., None])
            actual = fin_arr[y:y+h, x:x+w].astype(np.float64)
            composition_ok = bool(np.max(np.abs(expected-actual)) <= 2)
            text_luma = luminance(actual / 255.0)
        else:
            text_l = float(luminance(parse_color(b["color"]).reshape(1, 1, 3))[0, 0])
            text_luma = np.full_like(luma_bg, text_l)
        contrast = wcag(text_luma, luma_bg)[support]
        frac = float((contrast >= t["contrast"]).mean())
        ed = edge_density(luma_bg)
        ls = float(luma_bg.std())
        thumb_px = float(b.get("font_px", 0)) * args.scale

        reasons = []
        original = bg_pixels[y:y + h, x:x + w]
        changed = np.any(fin_arr[y:y + h, x:x + w] != original, axis=2)
        if not (changed & support).any():
            reasons.append("成品与底图在文字块内相同，未检测到文字渲染")
        if not composition_ok:
            reasons.append("文字层与背景的合成不匹配成品，不能用无关遮罩证明可读性")
        if frac < t["pass_fraction"]:
            reasons.append(f"对比度达标像素 {frac:.2f} < {t['pass_fraction']}（中位对比 {float(np.median(contrast)):.2f}）")
        warnings = []
        if ed > t["edge_density"]:
            warnings.append(f"背景边缘密度 {ed:.3f} > {t['edge_density']}，背景太花")
        if ls > t["luma_std"]:
            warnings.append(f"背景明度方差 {ls:.3f} > {t['luma_std']}，明暗不均")
        if thumb_px < t["min_thumb_px"]:
            reasons.append(f"缩略后字号 {thumb_px:.1f}px < {t['min_thumb_px']}px")

        verdict = "FAIL" if reasons else "PASS"
        if reasons:
            gate_fail = True
        results.append({
            "id": b["id"], "role": role, "verdict": verdict, "reasons": reasons, "warnings": warnings,
            "metrics": {
                "sampling": "glyph_alpha" if text_pixels is not None else "conservative_bbox",
                "sample_pixels": int(support.sum()),
                "composition_verified": composition_ok if text_pixels is not None else None,
                "contrast_median": round(float(np.median(contrast)), 2),
                "pass_fraction": round(frac, 3),
                "edge_density": round(ed, 3),
                "luma_std": round(ls, 3),
                "thumbnail_font_px": round(thumb_px, 1),
            },
        })

    report = {"limitations": "启发式检测；bbox模式保守。字形模式仍不能证明文字内容、实际字号、艺术字效果或构图正确，必须另做设计复核；纹理指标仅为复核提示", "gate": "FAIL" if gate_fail else "PASS", "scale": args.scale, "blocks": results}
    report["inputs"] = {"final_sha256": hashlib.sha256(Path(args.final).read_bytes()).hexdigest(), "background_sha256": hashlib.sha256(Path(args.background).read_bytes()).hexdigest(), "text_layer_sha256": hashlib.sha256(Path(args.text_layer).read_bytes()).hexdigest() if args.text_layer else None}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    if gate_fail:
        print("\n⛔ gate=FAIL：叠字可读性不达标。这是硬门禁，不能用构图分或配色分补偿。", file=sys.stderr)
        print("   先改：在主视觉内移位/断行，调整字重字号与颜色，必要时细描边/轻阴影或局部亮度处理；禁止为过检铺大块纯底、加页眉页脚或缩小主视觉。改完重跑。", file=sys.stderr)
    return 1 if gate_fail else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps({"gate": "ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
