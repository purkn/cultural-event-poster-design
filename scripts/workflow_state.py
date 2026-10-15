#!/usr/bin/env python3
"""Project-local checkpoints. Records evidence, not proof of human authorship."""
import argparse,json,hashlib
from pathlib import Path
CHECKPOINTS=('input','style','visual','feedback')
PHASE={'input':'input_review','style':'style_review','visual':'visual_review','feedback':'feedback_review'}
NEXT={'input':'strategy','style':'composition','visual':'production','feedback':'improvement_review'}
REQUIRED={'hero_a':('input','style'),'hero_b':('input','style'),'h0':('input','style','visual'),'repair':('input','style','visual'),'delivery':('input','style','visual')}
def fresh():
 return {'schema_version':1,'revision':1,'stage':'input_review','checkpoints':{k:{'status':'pending'} for k in CHECKPOINTS},'events':[]}
def decide(s,checkpoint,quote,selection=None,waived=False):
 if checkpoint not in CHECKPOINTS or not quote.strip():raise ValueError('checkpoint and actual user quote required')
 if s['checkpoints'][checkpoint]['status']!='pending':raise ValueError('decision already recorded; reopen to invalidate downstream choices')
 i=CHECKPOINTS.index(checkpoint)
 if any(s['checkpoints'][k]['status'] not in ('confirmed','waived') for k in CHECKPOINTS[:i]):raise ValueError('earlier checkpoint unresolved')
 if checkpoint=='feedback' and s['stage']!='feedback_review':raise ValueError('deliver files before feedback')
 if checkpoint in ('style','visual') and not selection and not waived:raise ValueError('explicit selection required')
 s['checkpoints'][checkpoint]={'status':'waived' if waived else 'confirmed','quote':quote,'selection':selection,'revision':s['revision']}
 s['stage']=NEXT[checkpoint];s['events'].append({'action':'decision','checkpoint':checkpoint,'quote':quote,'selection':selection,'waived':waived,'revision':s['revision']})
 return s
def invalidate(s,checkpoint,reason):
 if checkpoint not in CHECKPOINTS or not reason.strip():raise ValueError('checkpoint and reason required')
 for k in CHECKPOINTS[CHECKPOINTS.index(checkpoint):]:s['checkpoints'][k]={'status':'pending'}
 s['revision']+=1;s['stage']=PHASE[checkpoint];s['events'].append({'action':'invalidate','from':checkpoint,'reason':reason,'revision':s['revision']});return s
def guard(s,stage):
 if stage not in REQUIRED:raise ValueError('unknown guarded operation')
 missing=[k for k in REQUIRED[stage] if s['checkpoints'][k]['status'] not in ('confirmed','waived')]
 if missing:raise ValueError('unresolved checkpoints: '+', '.join(missing))
 if s['stage'] in ('feedback_review','improvement_review'):raise ValueError('delivered revision: reopen affected checkpoint before new production')
 return True
def main():
 p=argparse.ArgumentParser();p.add_argument('--state',required=True);p.add_argument('action',choices=['init','decide','reopen','guard','deliver']);p.add_argument('--checkpoint',choices=CHECKPOINTS);p.add_argument('--quote',default='');p.add_argument('--selection');p.add_argument('--waived',action='store_true');p.add_argument('--reason',default='');p.add_argument('--operation');a=p.parse_args();path=Path(a.state)
 try:
  if a.action=='init':
   if path.exists():raise ValueError('state already exists')
   s=fresh()
  else:
   s=json.loads(path.read_text(encoding='utf-8'))
   if a.action=='decide':s=decide(s,a.checkpoint,a.quote,a.selection,a.waived)
   elif a.action=='reopen':s=invalidate(s,a.checkpoint,a.reason)
   elif a.action=='guard':guard(s,a.operation);print(json.dumps({'allowed':True,'revision':s['revision']}));return
   elif a.action=='deliver':
    guard(s,'delivery')
    if not a.quote.strip():raise ValueError('actual delivered file paths and validation evidence required')
    s['stage']='feedback_review';s['events'].append({'action':'delivered','evidence':a.quote,'revision':s['revision']})
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
 except (ValueError,OSError,KeyError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
