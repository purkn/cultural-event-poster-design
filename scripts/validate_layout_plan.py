#!/usr/bin/env python3
"""Check layout plan geometry, not actual glyph fit or visual quality."""
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check(plan):
 errors=[];warnings=[]
 modes={m['id']:m for m in json.loads((ROOT/'libraries/layouts/spatial_modes.json').read_text())['modes']}
 masters={m['id'] for m in json.loads((ROOT/'libraries/layouts/templates.json').read_text())['layouts']}
 if plan.get('topology') not in masters:errors.append('unknown topology')
 mode=modes.get(plan.get('spatial_mode'))
 if not mode:errors.append('unknown spatial mode')
 canvas=plan.get('canvas')
 if not isinstance(canvas,list) or len(canvas)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) or v<=0 for v in canvas):errors.append('invalid canvas')
 else:
  orientation='portrait' if canvas[1]>canvas[0] else 'landscape' if canvas[0]>canvas[1] else 'square'
  if plan.get('orientation')!=orientation:errors.append('orientation does not match canvas')
  if mode and mode['orientation']!=orientation:errors.append('spatial mode does not match canvas; square needs adapted plan')
 for key in ['selection_reason','rejected_alternative','capacity_evidence','reading_path']:
  if not plan.get(key):errors.append('missing '+key)
 title=plan.get('title_skeleton',{})
 if not isinstance(title,dict) or not title.get('text') or not title.get('lines'):errors.append('missing accurate title skeleton')
 elif not isinstance(title['lines'],list) or any(not isinstance(s,str) for s in title['lines']) or ''.join(title['lines'])!=title['text']:errors.append('title lines must preserve exact text')
 valid={}
 for group in ['regions','protected_regions']:
  items=plan.get(group)
  if not isinstance(items,list):errors.append('missing '+group);continue
  if group=='regions' and not items:errors.append('empty regions')
  for i,item in enumerate(items):
   if not isinstance(item,dict):errors.append('invalid region');continue
   rect=[item.get(k) for k in ['x','y','w','h']]
   if any(type(v) not in (int,float) or not math.isfinite(v) for v in rect):errors.append('invalid region coordinates');continue
   x,y,w,h=rect
   if x<0 or y<0 or w<=0 or h<=0 or x+w>100 or y+h>100:errors.append('region outside normalized canvas');continue
   valid[(group,i)]=rect
   if not item.get('role'):errors.append('missing region role')
   if group=='regions' and ('z_order' not in item or type(item.get('allow_overlap')) is not bool):errors.append('missing region layer/overlap policy')
 for (g,i),a in valid.items():
  if g!='regions' or plan['regions'][i].get('role') not in ['title','body','facts']:continue
  for (pg,j),b in valid.items():
   if pg=='protected_regions' and a[0]<b[0]+b[2] and b[0]<a[0]+a[2] and a[1]<b[1]+b[3] and b[1]<a[1]+a[3]:warnings.append(f'region {i} intersects protected region {j}; inspect actual glyphs and subject')
 return {'status':'FAIL' if errors else 'REVIEW' if warnings else 'GEOMETRY_OK','errors':errors,'warnings':warnings,'limits':'Geometry only; does not certify text fit, actual occlusion or readability.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--plan',required=True);a=p.parse_args()
 try:r=check(json.loads(Path(a.plan).read_text()))
 except (OSError,ValueError,TypeError,AttributeError) as e:p.exit(2,str(e)+'\n')
 print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(1 if r['errors'] else 0)
if __name__=='__main__':main()
