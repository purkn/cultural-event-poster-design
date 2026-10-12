#!/usr/bin/env python3
"""Poster Plan -> portable SVG with editable SVG text objects.

Always validates exact title content, geometry, font presence and avoids
per-glyph CSS-trick variants. Does not claim visual/aesthetic approval.
"""
import argparse
import base64
import json
import math
import mimetypes
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)
SVG = lambda s: f"{{{SVG_NS}}}{s}"

class LayoutError(ValueError):
    pass


def numeric(value, field, positive=False):
    try:
        v = float(value)
        if not math.isfinite(v) or (positive and v <= 0): raise ValueError
        return v
    except (ValueError, TypeError):
        raise LayoutError(f"INVALID_NUMBER:{field}")


def txt(e):
    if not isinstance(e, str) or not e.strip(): raise LayoutError("EMPTY_TEXT")
    return e


def validate_color(s):
    if not isinstance(s, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}",s):
        raise LayoutError("INVALID_COLOR_USE_6_DIGIT_HEX")
    return s


def read_font(font):
    from PIL import ImageFont
    fp=Path(font.get("font_file", ""))
    if not fp.is_file(): raise LayoutError(f"FONT_FILE_MISSING:{fp}")
    face_index=int(font.get("face_index",0))
    if not font.get("font_family") or not isinstance(font["font_family"],str):
        raise LayoutError("FONT_FAMILY_MISSING")
    size=int(numeric(font.get("font_size"),"font_size",positive=True))
    try: f=ImageFont.truetype(str(fp),size,index=face_index)
    except (OSError,ValueError) as e: raise LayoutError(f"FONT_LOAD_ERROR:{e}")
    return f


def ensure_coverage(font, chars):
    """Best effort glyph coverage, distinct from actual shape acceptance."""
    try:
        from fontTools.ttLib import TTFont,TTCollection
    except ImportError:
        raise LayoutError("FONTTOOLS_MISSING:fontTools required for glyph coverage")
    fp=font['font_file'];face_index=int(font.get('face_index',0))
    owner = TTCollection(fp,lazy=True) if str(fp).lower().endswith(('.ttc','.otc')) else TTFont(fp,lazy=True)
    try:
        if isinstance(owner, TTCollection):
            if face_index<0 or face_index>=len(owner.fonts): raise LayoutError('FONT_FACE_INDEX_INVALID')
            face=owner.fonts[face_index]
        else:
            if face_index != 0: raise LayoutError('FONT_FACE_INDEX_INVALID')
            face=owner
        cmap={}
        for t in face['cmap'].tables:
            if t.isUnicode():cmap.update(t.cmap)
        miss=sorted(set(ch for ch in chars if not ch.isspace() and ord(ch) not in cmap))
        if miss: raise LayoutError('GLYPHS_MISSING:'+''.join(miss))
    finally:
        owner.close()


def estimate_text_width(font, line, fontconfig):
    # Pillow metrics approximate the browser/font-engine result; final screenshot needed.
    tracking=numeric(fontconfig.get('letter_spacing',0),'letter_spacing')
    return float(font.getlength(line))+max(0,len(line)-1)*tracking


def make_text_group(root, box, kind, canvas, safe):
    mode=box.get('mode','STANDARD_BLOCK')
    if kind=='h0' and mode not in ('STANDARD_BLOCK','CUSTOM_GLYPH'):
        raise LayoutError('INVALID_H0_MODE')
    # Explicitly disallow unverified per-glyph CSS-type transforms and size lists.
    forbidden=['per_character','per_glyph','char_sizes','char_rotations','rotate_chars','scale_chars','transform']
    if any(k in box for k in forbidden):raise LayoutError('PER_GLYPH_VARIATION_FORBIDDEN')
    raw=txt(box.get('text',''))
    x=numeric(box.get('x'),'x');y=numeric(box.get('y'),'y')
    max_w=numeric(box.get('max_width'),'max_width',positive=True)
    if (x<safe or y<safe or x+max_w>canvas['width']-safe+1):
        raise LayoutError(f'{kind.upper()}_REGION_OUTSIDE_SAFE_AREA')
    if kind=='h0' and mode=='CUSTOM_GLYPH':
        paths=box.get('custom_paths')
        if not box.get('reference_evidence') or not paths or not isinstance(paths,list):
            raise LayoutError('CUSTOM_GLYPH_NEEDS_REFERENCE_EVIDENCE_AND_PATHS')
        if ''.join(p.get('char','') for p in paths if isinstance(p,dict)) != raw:
            raise LayoutError('CUSTOM_GLYPH_TEXT_IDENTITY_MISMATCH')
        group=ET.SubElement(root,SVG('g'),{'id':'h0-custom-editable-paths','data-source-text':raw})
        ET.SubElement(group,SVG('title')).text=raw
        for i,p in enumerate(paths):
            if not isinstance(p,dict) or not isinstance(p.get('d'),str) or not re.fullmatch(r'[0-9eE+\-.,\sMmLlHhVvCcSsQqTtAaZz]+',p['d']):
                raise LayoutError('CUSTOM_PATH_INVALID')
            fill=validate_color(p.get('fill',box.get('fill','#000000')))
            ET.SubElement(group,SVG('path'),{'id':f'glyph-path-{i+1}','d':p['d'],'fill':fill})
        return
    font=read_font(box)
    lines=box.get('lines') or [raw]
    if not isinstance(lines,list) or not all(isinstance(s,str) and s for s in lines) or ''.join(lines)!=raw.replace('\n',''):
        raise LayoutError(f'{kind.upper()}_SOURCE_LINES_MISMATCH')
    if len(lines)>5: raise LayoutError('TOO_MANY_TEXT_LINES')
    ensure_coverage(box,raw)
    size=int(numeric(box.get('font_size'),'font_size',positive=True))
    spacing=numeric(box.get('line_spacing',size*1.2),'line_spacing',positive=True)
    if y+(len(lines)-1)*spacing+size*1.25>canvas['height']-safe:
        raise LayoutError(f'{kind.upper()}_VERTICAL_OVERFLOW')
    fontfam=box['font_family']
    color=validate_color(box.get('fill','#111111'))
    widths=[estimate_text_width(font,s,box) for s in lines]
    if any(w>max_w+1.5 for w in widths):
        raise LayoutError(f'{kind.upper()}_HORIZONTAL_OVERFLOW:font_or_layout_reselection_required')
    text=ET.SubElement(root,SVG('text'),{
        'id':re.sub('[^a-zA-Z0-9_-]','-',box.get('id','h0' if kind=='h0' else 'text')),
        'x':str(x),'y':str(y),'font-family':fontfam,'font-size':str(size),
        'font-weight':str(box.get('font_weight','normal')),'fill':color,
        'letter-spacing':str(box.get('letter_spacing',0)),'text-anchor':'start',
        'dominant-baseline':'hanging','xml:space':'preserve',
        'data-font-file':str(Path(box['font_file']).name),'data-font-face-index':str(box.get('face_index',0))
    })
    for i,line in enumerate(lines):
        sub=ET.SubElement(text,SVG('tspan'),{'x':str(x),'y':str(y+i*spacing)})
        sub.text=line
    return {'id':box.get('id',kind),'measured_width':max(widths,default=0),'height':(len(lines)-1)*spacing+size*1.2, 'x':x,'y':y}


def generate(plan, path):
    if not isinstance(plan,dict): raise LayoutError('INPUT_NOT_OBJECT')
    canvas=plan.get('canvas',{})
    W=int(numeric(canvas.get('width'),'canvas.width',positive=True))
    H=int(numeric(canvas.get('height'),'canvas.height',positive=True))
    if W<100 or H<100: raise LayoutError('INVALID_CANVAS')
    safe=numeric(canvas.get('safe_margin',25),'canvas.safe_margin')
    bg=validate_color(canvas.get('background','#FFFFFF'))
    frame={'width':W,'height':H}
    root=ET.Element(SVG('svg'),{'width':str(W),'height':str(H),'viewBox':f'0 0 {W} {H}','version':'1.1'})
    ET.SubElement(root,SVG('title')).text=plan.get('description','Poster — editable source')
    ET.SubElement(root,SVG('desc')).text='SVG text nodes are editable in source; some editors may outline them on import.'
    ET.SubElement(root,SVG('rect'),{'id':'background','x':'0','y':'0','width':str(W),'height':str(H),'fill':bg})
    if plan.get('hero'):
        h=plan['hero'];f=Path(h.get('file',''))
        if not f.is_file(): raise LayoutError(f'HERO_FILE_MISSING:{f}')
        if f.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):
            raise LayoutError('HERO_IMAGE_FORMAT_INVALID')
        mime=mimetypes.guess_type(str(f))[0] or 'image/png'
        b64=base64.b64encode(f.read_bytes()).decode('ascii')
        vals={k:numeric(h.get(k),f'hero.{k}') for k in ('x','y','width','height')}
        if vals['width']<=0 or vals['height']<=0:raise LayoutError('HERO_SIZE_INVALID')
        ET.SubElement(root,SVG('image'),{'id':'hero-raster-editable-position',**{k:str(v) for k,v in vals.items()},'preserveAspectRatio':'xMidYMid '+h.get('fit','slice'),'href':f'data:{mime};base64,{b64}'})
    shapes=plan.get('shapes',[])
    if shapes and not isinstance(shapes,list): raise LayoutError('SHAPES_NOT_LIST')
    for i,sh in enumerate(shapes):
        t=sh.get('type')
        if t=='rect':
            p={k:str(numeric(sh.get(k),f'shape.{k}')) for k in ('x','y','width','height')}
            ET.SubElement(root,SVG('rect'),{'id':f'shape-{i}',**p,'fill':validate_color(sh['fill'])})
        elif t=='line':
            p={k:str(numeric(sh.get(k),f'shape.{k}')) for k in ('x1','y1','x2','y2')}
            ET.SubElement(root,SVG('line'),{'id':f'shape-{i}',**p,'stroke':validate_color(sh['stroke']),'stroke-width':str(numeric(sh.get('stroke_width',1),'stroke_width',positive=True))})
        else: raise LayoutError('SHAPE_TYPE_NOT_SUPPORTED')
    # v0.19: composited behind editable text, bounded and explicitly authorized.
    # Local translucent tint is never a default black scrim.
    tweaks=plan.get('local_readability_treatments',[])
    pol=plan.get('readability_policy',{})
    if tweaks:
        if 'local_tint' not in pol.get('allowed_treatments',[]):
            raise LayoutError('LOCAL_TREATMENT_NOT_AUTHORIZED')
        allowed=float(pol.get('max_tint_opacity',0.16))
        if allowed<=0 or allowed>0.20:raise LayoutError('INVALID_TINT_OPACITY_CAP')
        for idx,t in enumerate(tweaks):
            x=numeric(t['x'],'tint.x');y=numeric(t['y'],'tint.y')
            w=numeric(t['width'],'tint.width',positive=True)
            h=numeric(t['height'],'tint.height',positive=True)
            alpha=numeric(t['opacity'],'tint.opacity',positive=True)
            if alpha>allowed+0.00001 or w*h>W*H*float(pol.get('max_tint_area_ratio',0.10)):
                raise LayoutError('LOCAL_TREATMENT_EXCEEDS_STYLE_BUDGET')
            if x<0 or y<0 or x+w>W or y+h>H:raise LayoutError('LOCAL_TREATMENT_OUTSIDE_CANVAS')
            fill=validate_color(t['fill'])
            defs=root.find(SVG('defs'))
            if defs is None:defs=ET.SubElement(root,SVG('defs'))
            gid=f'local-tint-fade-{idx}'
            grad=ET.SubElement(defs,SVG('linearGradient'),{
                'id':gid,'x1':'0%','x2':'100%','y1':'0%','y2':'0%'})
            for off,opa in [('0%',0),('13%',alpha),('87%',alpha),('100%',0)]:
                ET.SubElement(grad,SVG('stop'),{
                    'offset':off,'stop-color':fill,'stop-opacity':str(opa)})
            ET.SubElement(root,SVG('rect'),{
                'id':f'local-readability-treatment-{idx}',
                'x':str(x),'y':str(y),'width':str(w),'height':str(h),
                'fill':f'url(#{gid})','pointer-events':'none'})
    if 'h0' not in plan: raise LayoutError('H0_MISSING')
    metrics=[]
    m=make_text_group(root,plan['h0'],'h0',frame,safe)
    if m: metrics.append(m)
    blocks=plan.get('text_blocks',[])
    if not isinstance(blocks,list): raise LayoutError('TEXT_BLOCKS_NOT_LIST')
    for b in blocks:
        if b.get('mode')=='CUSTOM_GLYPH': raise LayoutError('BODY_CUSTOM_GLYPH_FORBIDDEN')
        m=make_text_group(root,b,'body',frame,safe)
        if m:metrics.append(m)
    # Text-text collisions are always unintended in the basic plan.
    for i,a in enumerate(metrics):
        for b in metrics[i+1:]:
            if (a['x'] < b['x']+b['measured_width'] and b['x'] < a['x']+a['measured_width'] and
                a['y'] < b['y']+b['height'] and b['y'] < a['y']+a['height']):
                raise LayoutError(f"TEXT_BLOCK_COLLISION:{a['id']}:{b['id']}")
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    return metrics


def cli():
    ap=argparse.ArgumentParser(description='SVG-first fixed poster compositor with editable text')
    ap.add_argument('plan',type=Path)
    ap.add_argument('output',type=Path)
    ap.add_argument('--png',type=Path)
    args=ap.parse_args()
    try:
        inp=json.loads(args.plan.read_text(encoding='utf-8'))
        ms=generate(inp,args.output)
        if args.png:
            try:import cairosvg
            except ImportError: raise LayoutError('CAIROSVG_NOT_INSTALLED')
            args.png.parent.mkdir(parents=True,exist_ok=True)
            cairosvg.svg2png(url=str(args.output),write_to=str(args.png))
        print(json.dumps({'status':'DRAFT_ONLY_REQUIRES_FINAL_COMPOSITE_AUDIT','svg':str(args.output),'png':str(args.png) if args.png else None,'metrics':ms},ensure_ascii=False))
    except (LayoutError,json.JSONDecodeError,OSError,KeyError) as e:
        print('LAYOUT_FAIL: '+str(e),file=sys.stderr)
        sys.exit(2)

if __name__=='__main__':cli()
