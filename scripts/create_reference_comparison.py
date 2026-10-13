#!/usr/bin/env python3
"""Contact-sheet proof. Does not evaluate aesthetic quality or claim similarity. Requires Pillow."""
import argparse, json
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont

def create(lead,generated,out):
    inputs=[('LEAD REFERENCE',Path(lead)),('GENERATED ROUGH / ACTUAL OUTPUT',Path(generated))]
    tile=(520,750); margin=26
    board=Image.new('RGB',(tile[0]*2+margin*3,tile[1]+margin*2+62),'white')
    draw=ImageDraw.Draw(board)
    for n,(label,path) in enumerate(inputs):
        if not path.is_file():raise FileNotFoundError(str(path))
        im=Image.open(path).convert('RGB')
        thumb=ImageOps.contain(im,tile)
        x=margin+n*(tile[0]+margin)+(tile[0]-thumb.width)//2
        y=margin+(tile[1]-thumb.height)//2
        board.paste(thumb,(x,y));draw.text((margin+n*(tile[0]+margin),margin+tile[1]+12),label,fill='#111111')
    draw.text((margin,margin+tile[1]+37),'EVIDENCE ONLY - NO DESIGN PASS WITHOUT REAL VISUAL CRITIQUE',fill='#9B2525')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);board.save(out)
    report={'status':'SIDE_BY_SIDE_CREATED','design_pass':'NOT_ASSESSED','sources':{'lead':str(lead),'generated':str(generated)},'note':'Human/vision comparison required; no aesthetic verdict from script.'}
    out.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--lead',required=True);p.add_argument('--generated',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(create(a.lead,a.generated,a.out))
