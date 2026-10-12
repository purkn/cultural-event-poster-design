#!/usr/bin/env python3
"""Offline font face & glyph coverage checker. Does not install or download fonts."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

def _get_font(font_path, face_index=0):
    from fontTools.ttLib import TTFont, TTCollection
    p=Path(font_path)
    if p.suffix.lower() in ('.ttc','.otc'):
        coll=TTCollection(str(p),lazy=False)
        if not 0 <= face_index < len(coll.fonts):
            raise IndexError(f'face {face_index} not present; face_count={len(coll.fonts)}')
        return coll.fonts[face_index],len(coll.fonts)
    if face_index != 0: raise IndexError('single-face font supports only index=0')
    return TTFont(str(p),lazy=False),1

def assess(font_path, text, face_index=0, locale=None):
    p=Path(font_path)
    if not p.is_file():raise FileNotFoundError(font_path)
    font,face_count=_get_font(p,face_index)
    cmap=set()
    for tab in font['cmap'].tables:
        if tab.isUnicode():cmap.update(tab.cmap.keys())
    missing=[]; present=[]
    for ch in dict.fromkeys(text):
        if ch.isspace():continue
        (present if ord(ch) in cmap else missing).append({'char':ch,'codepoint':f'U+{ord(ch):04X}'})
    names=font['name'].names if 'name' in font else []
    def get_name(name_id):
        for n in names:
            if n.nameID==name_id:
                try:return n.toUnicode()
                except Exception:continue
        return None
    family=get_name(1) or ''
    # A TTC may contain JP/KR/SC/TC regional glyph variants with identical unicode coverage.
    # Cmap success alone cannot prove the proper Chinese regional forms were selected.
    region=next((x for x in [' JP',' KR',' SC',' TC',' HK'] if family.endswith(x)),None)
    wanted={'zh-CN':' SC','zh-SG':' SC','zh-TW':' TC','zh-HK':' HK','ja-JP':' JP','ko-KR':' KR'}.get(locale)
    locale_match=(region==wanted) if region and wanted else None
    result={
      'font_file':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'font_family':get_name(1),'locale_requested':locale,'regional_face_match':locale_match,'font_subfamily':get_name(2),'postscript_name':get_name(6),
      'face_index':face_index,'face_count':face_count,'text':text,'glyphs_checked':len(present)+len(missing),
      'missing':missing,'covered':present,'coverage_ok':not bool(missing) and locale_match is not False,
      'browser_font_loaded':'NOT_VERIFIED','visual_reference_match':'NOT_VERIFIED',
      'note':'cmap presence does not prove shape quality, licensing, or browser use'
    }
    font.close()
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--font',required=True);ap.add_argument('--text',required=True)
    ap.add_argument('--face',type=int,default=0);ap.add_argument('--locale',default='zh-CN');ap.add_argument('--out')
    a=ap.parse_args()
    try:r=assess(a.font,a.text,a.face,a.locale)
    except Exception as exc:print(json.dumps({'status':'ERROR','error':str(exc)},ensure_ascii=False));return 2
    output=json.dumps(r,ensure_ascii=False,indent=2)
    if a.out:Path(a.out).write_text(output+'\n',encoding='utf-8')
    print(output)
    return 0 if r['coverage_ok'] else 1

if __name__=='__main__':sys.exit(main())
