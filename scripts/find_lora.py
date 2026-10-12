#!/usr/bin/env python3
"""Search Hugging Face public repository metadata ONLY; NEVER downloads weights.

Online mode requires network access; offline mode reads verified model registry metadata.
Results are unverified *candidates*, not downloadable approvals or model recommendations.
"""
import json,argparse,urllib.request,urllib.parse
from pathlib import Path

def search_online(query,limit,timeout=12):
    args=urllib.parse.urlencode({'search':query,'limit':min(limit,20),'full':'true'})
    url='https://huggingface.co/api/models?'+args
    req=urllib.request.Request(url,headers={'User-Agent':'PosterSkill-LoRAMetadataSearch/0.14'})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=json.loads(r.read(3_000_000))
    result=[]
    for it in data:
        repo=it.get('id','');tags=it.get('tags',[])
        # Search result can mix full models and adapters. Do not claim it IS a LoRA without evidence.
        if not any('lora' in str(tag).lower() for tag in tags+[repo]):continue
        card=it.get('cardData') or {}
        result.append({'repo_id':repo,'tags':tags[:15], 'license_claim':card.get('license'),
                       'base_model_claim':card.get('base_model'), 'revision':it.get('sha'),
                       'status':'UNVERIFIED_CANDIDATE', 'downloaded':False,
                       'note':'Need exact weight, size, visual samples, license rights, base model verification before consent request.'})
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--query',required=True);p.add_argument('--base-family',default='');p.add_argument('--limit',type=int,default=5);p.add_argument('--offline',action='store_true');p.add_argument('--registry',default=str(Path(__file__).resolve().parents[1]/'model_adapters/registry.json'))
    a=p.parse_args()
    if a.offline:
        data=json.loads(Path(a.registry).read_text(encoding='utf-8'))
        cand=data.get('verified_adapters',[])+data.get('experimental_candidates',[])
        res=[x for x in cand if a.query.lower() in json.dumps(x,ensure_ascii=False).lower()]
    else:
        try:res=search_online(' '.join(s for s in [a.query,'lora',a.base_family] if s),a.limit)
        except Exception as e:
            print(json.dumps({'status':'SEARCH_UNAVAILABLE','error':str(e),'fallback':'use reference-only generation; no model download'},ensure_ascii=False,indent=2));return
    print(json.dumps({'status':'CANDIDATES_ONLY','models':res[:a.limit],'downloads':0},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
