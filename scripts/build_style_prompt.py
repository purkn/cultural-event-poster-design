#!/usr/bin/env python3
"""Expand a local S1–S8 guide template; no network or image generation calls."""
import argparse,json,re,string
from pathlib import Path
from workflow_state import guard
ROOT=Path(__file__).resolve().parents[1]
def templates(style):
 packs=json.loads((ROOT/'libraries/styles/packs.json').read_text(encoding='utf-8'))['packs']
 pack=next((p for p in packs if p['id']==style),None)
 if not pack:raise ValueError('style must be canonical S1–S8')
 guide=(ROOT/pack['guide']).read_text(encoding='utf-8')
 blocks=re.findall(r'```json\s*\n(.*?)\n```',guide,re.S)
 data=[json.loads(b) for b in blocks if '"prompts"' in b]
 if len(data)!=1:raise ValueError('guide must contain one runtime template source')
 return data[0]['prompts']
def expand(style,stage,values):
 table=templates(style)
 if stage not in table:raise ValueError('invalid stage')
 spec=table[stage];required={name for _,name,_,_ in string.Formatter().parse(spec['prompt']) if name}
 missing=sorted(k for k in required if not isinstance(values.get(k),str) or not values[k].strip())
 if missing:raise ValueError('missing confirmed blueprint values: '+', '.join(missing))
 result=spec['prompt'].format_map(values)
 return {'style':style,'stage':stage,'prompt':result,'transparency_intent':spec['transparent_background'],'note':'提示词准备结果；并未生成图片、确认断点或证明参考已送入后端'}
def main():
 a=argparse.ArgumentParser();a.add_argument('--state',required=True);a.add_argument('--style',required=True);a.add_argument('--stage',required=True,choices=['hero_a','hero_b','h0','repair']);a.add_argument('--values',required=True);a.add_argument('--out');args=a.parse_args()
 try:
  guard(json.loads(Path(args.state).read_text(encoding='utf-8')),args.stage)
  r=expand(args.style,args.stage,json.loads(Path(args.values).read_text(encoding='utf-8')))
 except (ValueError,OSError) as exc:a.exit(2,str(exc)+'\n')
 data=json.dumps(r,ensure_ascii=False,indent=2)
 if args.out:Path(args.out).write_text(data,encoding='utf-8')
 print(data)
if __name__=='__main__':main()
