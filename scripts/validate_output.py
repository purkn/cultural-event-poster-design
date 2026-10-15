#!/usr/bin/env python3
"""Validate actual layer outputs and evidence records; cannot verify OCR or beauty."""
import argparse,json,math,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
from compose_layers import load_layers

def validate(project,lang):
    project=Path(project);issues=[]
    if not lang or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in lang):return ['invalid language filename token']
    def read(rel):return json.loads((project/rel).read_text(encoding='utf-8'))
    try:
        a,b,c=load_layers(project/f'02_hero/hero_{lang}.png',project/f'03_title/title_{lang}.png',project/f'04_text/text_{lang}.png')
        expected=Image.alpha_composite(Image.alpha_composite(a,b),c).convert('RGB');actual=Image.open(project/f'01_final/poster_{lang}.png').convert('RGB')
        if expected.size!=actual.size or expected.tobytes()!=actual.tobytes():issues.append('final differs from actual layer composition')
        combined=Image.open(project/f'06_metadata/text_combined_{lang}.png').convert('RGBA')
        if combined.size!=a.size or combined.tobytes()!=Image.alpha_composite(b,c).tobytes():issues.append('combined text mask differs from text layers')
        if not (project/f'05_source/layers_{lang}.svg').is_file():issues.append('missing source project')
        body_source=project/f'05_source/text_{lang}.svg'
        if not body_source.is_file():issues.append('missing editable body text source')
        else:
            tree=ET.parse(body_source)
            text_nodes=[n for n in tree.iter() if n.tag.split('}')[-1]=='text' and ''.join(n.itertext()).strip()]
            if not text_nodes:issues.append('body source has no live editable text')
        activity=read('06_metadata/activity.json');fields=activity.get('fields',{})
        for key in ('theme','languages','purpose','output_dimensions','dates','venue_or_online','organizer','description','audience','registration'):
            v=fields.get(key,{})
            status=v.get('status')
            if status not in ('provided','inferred','fictional','not_applicable'):issues.append('unresolved content: '+key);continue
            if status=='not_applicable':
                if key in ('theme','languages','purpose','output_dimensions') or not v.get('reason'):issues.append('invalid not_applicable: '+key)
            elif v.get('value') in (None,'',[]):issues.append('missing value: '+key)
            if not v.get('source'):issues.append('missing content source: '+key)
            if status=='fictional' and not activity.get('fiction_authorization'):issues.append('fiction without authorization: '+key)
            if status=='inferred' and not v.get('confirmed'):issues.append('inferred content not confirmed: '+key)
        dimensions=fields.get('output_dimensions',{}).get('value')
        if dimensions!=list(a.size):issues.append('canvas does not match approved output_dimensions')
        langs=fields.get('languages',{}).get('value',[])
        if not isinstance(langs,list) or lang not in langs:issues.append('language outside approved brief')
        q=read(f'06_metadata/quality_{lang}.json')
        for key in ('text_accuracy','readability','layer_integrity','content_completeness'):
            item=q.get('hard_gates',{}).get(key,{})
            if item.get('status')!='PASS' or not item.get('evidence'):issues.append('hard gate not verified: '+key)
        for key in ('design_quality','style_consistency'):
            item=q.get('aesthetics',{}).get(key,{});score=item.get('score')
            if type(score) not in (int,float) or not math.isfinite(score) or not 1<=score<=5 or not item.get('evidence'):issues.append('missing aesthetic assessment: '+key)
        d=q.get('design_review',{})
        if d.get('verdict')!='PASS' or not d.get('evidence'):issues.append('design review not passed')
        report=read(f'06_metadata/readability_{lang}.json')
        if report.get('gate')!='PASS' or not report.get('blocks'):issues.append('readability report not passed')
        for key,rel in [('final_sha256',f'01_final/poster_{lang}.png'),('background_sha256',f'02_hero/hero_{lang}.png'),('text_layer_sha256',f'06_metadata/text_combined_{lang}.png')]:
            if report.get('inputs',{}).get(key)!=hashlib.sha256((project/rel).read_bytes()).hexdigest():issues.append('stale/mismatched readability report: '+key)
        state=read('06_metadata/workflow_state.json')
        if state.get('pending_checkpoint') not in (None,''):issues.append('production checkpoint still pending')
        if state.get('schema_version')!=1:issues.append('workflow state requires current schema; recheck actual confirmations')
        for key in ('input','style','visual'):
            record=state.get('checkpoints',{}).get(key,{})
            if record.get('status') not in ('confirmed','waived') or not record.get('quote'):issues.append('missing user decision/waiver: '+key)
            if key in ('style','visual') and record.get('status')=='confirmed' and not record.get('selection'):issues.append('missing selected option: '+key)
    except (OSError,ValueError,TypeError,KeyError,AttributeError,ET.ParseError) as exc:issues.append('invalid/missing artifact: '+str(exc))
    return issues

def main():
    a=argparse.ArgumentParser();a.add_argument('--project',required=True);a.add_argument('--language',required=True);args=a.parse_args();issues=validate(args.project,args.language)
    print(json.dumps({'status':'FAIL' if issues else 'PASS','issues':issues,'limits':'核验文件和记录结构；不独立证明文字语义、美学或用户原话真实性'},ensure_ascii=False,indent=2));raise SystemExit(1 if issues else 0)
if __name__=='__main__':main()
