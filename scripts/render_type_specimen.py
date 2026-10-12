#!/usr/bin/env python3
"""Generate exact-title PNG font specimen from a local font file; no model inference."""
import argparse, json, sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from font_coverage import assess

def make_proof(font_path, title, outfile, face_index=0, direction='vertical', locale='zh-CN', bg='#F8F6F2', fg='#1C1C1C'):
    report=assess(font_path,title,face_index,locale)
    if not report['coverage_ok']:raise ValueError('missing characters: '+''.join(x['char'] for x in report['missing']))
    W,H=960,1200
    pic=Image.new('RGB',(W,H),bg);draw=ImageDraw.Draw(pic)
    font=ImageFont.truetype(str(font_path),190,index=face_index)
    note_font=ImageFont.truetype(str(font_path),30,index=face_index)
    draw.text((65,48),'H0 FONT PROOF',fill=fg,font=note_font)
    glyphs=[c for c in title if not c.isspace()]
    if direction=='vertical':
        if not glyphs: raise ValueError('empty title')
        step=min(235,int(950/len(glyphs)))
        # Each glyph is centrally aligned by its actual bbox; does not try to imitate an artwork.
        y=190
        for ch in glyphs:
            b=draw.textbbox((0,0),ch,font=font)
            ww=b[2]-b[0];xx=int(W/2-ww/2)-b[0]
            draw.text((xx,y-b[1]),ch,fill=fg,font=font)
            y+=step
    else:
        bbox=draw.textbbox((0,0),title,font=font)
        text_w=bbox[2]-bbox[0];text_h=bbox[3]-bbox[1]
        if text_w>W-100:
            font=ImageFont.truetype(str(font_path),max(40,int(190*(W-100)/text_w)),index=face_index)
            bbox=draw.textbbox((0,0),title,font=font)
            text_w=bbox[2]-bbox[0];text_h=bbox[3]-bbox[1]
        draw.text((W/2-text_w/2-bbox[0],H/2-text_h/2-bbox[1]),title,font=font,fill=fg)
    draw.rectangle((40,40,W-40,H-40),outline='#B9B2A7',width=2)
    Path(outfile).parent.mkdir(parents=True,exist_ok=True)
    pic.save(outfile)
    return {'out':str(Path(outfile).resolve()),'title':title,'family':report['font_family'],'face_index':face_index,'font_sha256':report['sha256'],'note':'Specimen is proof of glyphs, not final typography or reference match'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--font',required=True);ap.add_argument('--text',required=True);ap.add_argument('--face',type=int,default=0)
    ap.add_argument('--direction',choices=['vertical','horizontal'],default='vertical');ap.add_argument('--locale',default='zh-CN');ap.add_argument('--out',required=True)
    args=ap.parse_args()
    try: print(json.dumps(make_proof(args.font,args.text,args.out,args.face,args.direction,args.locale),ensure_ascii=False,indent=2));return 0
    except Exception as e:print(str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
