#!/usr/bin/env python3
"""Validated multi-route visual prompt compiler. No model calls, downloads, or image QA.
Usage: python scripts/compile_routes_v017.py /path/project.json /path/output
Python >= 3.9; standard library only.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

class RouteError(Exception):
    def __init__(self, codes):
        self.codes=list(dict.fromkeys(codes))
        super().__init__('; '.join(self.codes))

def clean(s):
    if isinstance(s,(dict,list)): return json.dumps(s,ensure_ascii=False)
    return re.sub(r'[\x00-\x1f]',' ',str(s if s is not None else '')).strip()

def valid_source(path,root):
    try:
        p=(root/path).resolve()
        return p.is_file() and p.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.svg')
    except (TypeError,ValueError):return False

def text_from_parts(parts):
    return '\n\n'.join(parts)

def compile_routes(data, root, input_location=None):
    errors=[];warnings=[];root=Path(root).resolve()
    if data.get('schema_version')!='0.17':errors.append('SCHEMA_VERSION_NOT_017')
    if data.get('mode') not in ('hero_rough','h0_artword'):errors.append('INVALID_MODE')
    b=data.get('brief',{});can=data.get('canvas',{});backend=data.get('backend',{})
    if not isinstance(b,dict) or not b.get('confirmed') or not all(b.get(k) for k in ('title','date','venue','core_experience')):
        errors.append('BP_CONTENT_MISSING')
    try:
        width,height=int(can['width']),int(can['height'])
        if width<256 or height<256:errors.append('INVALID_CANVAS')
    except (KeyError,TypeError,ValueError):errors.append('INVALID_CANVAS');width=height=0
    if not all(isinstance(backend.get(k),bool) for k in ('supports_reference_images','supports_external_lora','supports_negative_prompt')):
        errors.append('BACKEND_CAPABILITIES_NOT_VERIFIED')
    if input_location:
        path=Path(input_location).resolve()
        if any(p.lower() in ('examples','samples','sample','golden','fixtures','test','tests') for p in path.parts):
            errors.append('PRODUCTION_INPUT_CANNOT_USE_EXAMPLE_FILE')
    routes=data.get('routes',[])
    if not isinstance(routes,list) or len(routes)<2:
        errors.append('AT_LEAST_TWO_DIFFERENT_ROUTES_REQUIRED');routes=routes if isinstance(routes,list) else []
    feedback=data.get('feedback') or {}
    if feedback and feedback.get('project_id')!=data.get('project_id'):
        errors.append('FEEDBACK_PROJECT_MISMATCH')
    if feedback.get('rejected') and not feedback.get('previous_route'):
        errors.append('REJECTED_FEEDBACK_NEEDS_PREVIOUS_ROUTE')
    prior=feedback.get('previous_route') or {}
    required_change=feedback.get('must_change',[]) if feedback.get('rejected') else []
    fingerprints=[];compiled=[];route_ids=set()
    for i,r in enumerate(routes):
        tag=f'R{i+1}'
        if not isinstance(r,dict):errors.append(f'{tag}:INVALID_ROUTE');continue
        lid=clean(r.get('id',''))
        if not lid or lid in route_ids:errors.append(f'{tag}:DUPLICATE_OR_MISSING_ID')
        route_ids.add(lid)
        lead=r.get('lead',{});col=r.get('color',{});typ=r.get('typography',{});concept=r.get('concept',{});comp=r.get('composition',{})
        for name,obj in [('lead',lead),('color',col),('typography',typ),('concept',concept),('composition',comp)]:
            if not isinstance(obj,dict):errors.append(f'{tag}:INVALID_{name.upper()}')
        if not all(isinstance(x,dict) for x in (lead,col,typ,concept,comp)):continue
        if not valid_source(lead.get('path',''),root):errors.append(f'{tag}:LEAD_IMAGE_NOT_FOUND')
        if lead.get('observed') is not True or len(clean(lead.get('observation_note','')))<15:
            errors.append(f'{tag}:LEAD_NOT_VISUALLY_OBSERVED')
        if not all(lead.get(k) for k in ('id','palette_family','value_regime','medium','type_dna','structure')):
            errors.append(f'{tag}:LEAD_DNA_INCOMPLETE')
        for k in ('palette_family','background_family','background','dominant','source'):
            if not col.get(k):errors.append(f'{tag}:COLOR_FIELD_MISSING:{k}')
        if col.get('source') not in ('lead','user_asset','art_direction'):
            errors.append(f'{tag}:COLOR_SOURCE_INVALID')
        if col.get('source')=='lead' and col.get('palette_family')!=lead.get('palette_family'):
            errors.append(f'{tag}:LEAD_COLOR_PROVENANCE_CONFLICT')
        if col.get('source')!='lead' and lead.get('classification')=='STRONG_LEAD' and col.get('palette_family')!=lead.get('palette_family'):
            errors.append(f'{tag}:STRONG_LEAD_OVERRIDE_WITHOUT_REROUTE')
        if not all(typ.get(k) for k in ('type_family','strategy','h0_design_action','reference_reason')):
            errors.append(f'{tag}:H0_NOT_DESIGNED')
        if typ.get('strategy') not in ('verified_custom_artword','reference_led_display','image_integrated'):
            errors.append(f'{tag}:TYPE_STRATEGY_INVALID')
        if not all(concept.get(k) for k in ('id','hero_subject','visible_mechanism','theme_binding')):
            errors.append(f'{tag}:VISUAL_MECHANISM_INCOMPLETE')
        if not all(comp.get(k) for k in ('hero_zone','h0_zone','info_zone','negative_space')):
            errors.append(f'{tag}:COMPOSITION_INCOMPLETE')
        if not r.get('reference_fit_reason') or len(clean(r['reference_fit_reason']))<15:
            errors.append(f'{tag}:ROUTE_REASON_NOT_SUBSTANTIVE')
        if not isinstance(r.get('negative_constraints'),list):errors.append(f'{tag}:MISSING_NEGATIVES')
        signature={'lead_id':clean(lead.get('id')),'palette_family':clean(col.get('palette_family')),'background_family':clean(col.get('background_family')),
                   'type_family':clean(typ.get('type_family')),'concept_id':clean(concept.get('id')),
                   'medium':clean(lead.get('medium'))}
        fingerprints.append(signature)
        if feedback.get('rejected'):
            for field in required_change:
                if field not in signature:errors.append(f'{tag}:INVALID_MUST_CHANGE_FIELD:{field}')
                elif signature[field].casefold()==clean(prior.get(field)).casefold():
                    errors.append(f'{tag}:USER_REJECTED_PATTERN_REUSED:{field}')
        if data.get('mode')=='h0_artword':
            glyph=typ.get('verified_glyph_path')
            if not glyph or not valid_source(glyph,root) or typ.get('glyph_verified') is not True:
                errors.append(f'{tag}:H0_REQUIRES_VERIFIED_CHARACTER_SKELETON')
        lines=[
          '[ROLE / TASK]\nGenerate one art-directed vertical poster HERO rough, not an entire advertisement. Do not render real title, dates, venue or logos.' if data.get('mode')!='h0_artword' else '[ROLE / TASK]\nCreate one standalone title graphic ONLY from the supplied verified glyph skeleton; preserve every exact character.',
          f'[EVENT EXPERIENCE]\n{clean(b.get("title"))}: {clean(b.get("core_experience"))}. Format {width}x{height}. Follow the specific visual mechanism, not a shopping list of theme nouns.',
          f'[CURRENT LEAD VISUAL WORLD]\nLead {clean(lead.get("id"))}; observed reference characteristics: {clean(lead.get("observation_note"))}.\nTopology: {clean(lead.get("structure"))}.\nMaterial: {clean(lead.get("medium"))}.\nLight/value: {clean(lead.get("value_regime"))}.\nTypography character: {clean(lead.get("type_dna"))}.\nThe lead image must actually be attached by capable backends; its subject and branded graphics are not to be copied.',
          f'[ONE DISTINCT CREATIVE MECHANISM]\n{clean(concept.get("visible_mechanism"))}\nHero subject: {clean(concept.get("hero_subject"))}.\nTheme-specific binding: {clean(concept.get("theme_binding"))}. No unrelated motifs.',
          f'[COMPOSITION / HIERARCHY]\nHero: {clean(comp.get("hero_zone"))}. H0 reserve: {clean(comp.get("h0_zone"))}. Metadata reserve: {clean(comp.get("info_zone"))}. Functional blank area: {clean(comp.get("negative_space"))}.',
          f'[COLOR CONTRACT — NO AUTOMATIC SEMANTIC COLORS]\nPalette family: {clean(col.get("palette_family"))}. Evidence source: {clean(col.get("source"))}.\nBackground: {clean(col.get("background"))} [{clean(col.get("background_family"))}]. Main: {clean(col.get("dominant"))}. Supporting: {clean(col.get("secondary","none"))}.\nDo not invent parchment, blues/reds, or other colors from theme labels.',
          f'[CHINESE H0 / VISUAL INTEGRATION]\nAccurate title later: {clean(b.get("title"))}. Visual type route: {clean(typ.get("strategy"))}; glyph family: {clean(typ.get("type_family"))}; structural design action: {clean(typ.get("h0_design_action"))}. The title is not acceptable if it is merely a large installed font. Reserve its actual composition footprint now.',
          '[FAILURE APPEARANCES]\n'+'\n'.join('- '+clean(x) for x in r.get('negative_constraints',[]))+'\nDo not inherit styling from example JSON files or previous rejected outputs.',
          '[FINAL GENERATED ASSET]\nOutput only the requested visual layer. Composition must work alongside precisely rendered Chinese title and factual metadata. Do not claim quality approval before actual visual review.'
        ]
        if feedback.get('rejected'):
            lines.insert(1,'[USER REJECTION / DO NOT REPEAT]\nPrevious attempt was rejected by the user. Do not reuse: '+ '; '.join(clean(x) for x in feedback.get('disliked_appearances',[])))
        if data.get('mode')=='h0_artword':
            lines.append('[VERIFIED GLYPH SOURCE]\nApply changes to the actual provided glyph image; no invented Hanzi: '+clean(typ.get('verified_glyph_path')))
        if not backend.get('supports_negative_prompt'):
            lines.append('[BACKEND CAPABILITY]\nNo separate negative prompt channel; the visible failure conditions above remain binding constraints.')
        compiled.append({'id':lid, 'status':'COMPILED_NOT_RENDERED', 'lead_id':lead.get('id'), 'route_fingerprint':signature,
                        'positive_prompt':text_from_parts(lines),
                        'negative_prompt':r.get('negative_constraints') if backend.get('supports_negative_prompt') else None,
                        'required_image_attachments':([
                           {'role':'lead','path':str((root/lead['path']).resolve()),'must_send_at_runtime':True}]
                           if backend.get('supports_reference_images') else [])+
                          ([{'role':'verified_glyph','path':str((root/typ['verified_glyph_path']).resolve()),'must_send_at_runtime':True}]
                           if data.get('mode')=='h0_artword' and typ.get('verified_glyph_path') else [])})
    if len(set((s['lead_id'],s['palette_family'],s['type_family'],s['concept_id']) for s in fingerprints))<len(fingerprints):
        errors.append('ROUTES_ARE_DUPLICATES_NOT_REAL_COMPARISON')
    if errors:raise RouteError(errors)
    if not backend.get('supports_reference_images'):
        warnings.append('TEXT_ONLY_REFERENCE_FALLBACK:visual_match_unverified')
    if not backend.get('supports_external_lora'):
        warnings.append('BASELINE_ONLY:external_lora_not_supported')
    else:
        warnings.append('LORA_OPTIONAL:only_after_license_compatibility_user_download_approval_and_runtime_verification')
    return {'schema_version':'0.17','project_id':data.get('project_id'), 'compile_status':'COMPILED_NOT_RENDERED',
            'design_status':'NOT_VISUALLY_REVIEWED','feedback_applied':bool(feedback.get('rejected')),
            'backend':{'id':backend.get('id'), 'reference_conditioning':'REQUESTED_NOT_VERIFIED' if backend.get('supports_reference_images') else 'TEXT_ONLY_REFERENCE_FALLBACK',
                       'lora_route':'OPTIONAL_AUTHORIZED_ONLY' if backend.get('supports_external_lora') else 'BASELINE_ONLY'},
            'warnings':warnings,'routes':compiled}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_json',type=Path);p.add_argument('out_dir',type=Path)
    args=p.parse_args();data=json.loads(args.input_json.read_text(encoding='utf-8'))
    try:out=compile_routes(data,args.input_json.parent,args.input_json)
    except RouteError as e:
        print('NEED_NEW_ROUTE: '+' | '.join(e.codes));return 2
    args.out_dir.mkdir(parents=True,exist_ok=True)
    (args.out_dir/'route_prompt_pack.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for item in out['routes']:
        name=re.sub('[^a-zA-Z0-9_-]','_',item['id'])
        (args.out_dir/(f'route_{name}.txt')).write_text(item['positive_prompt'],encoding='utf-8')
    print('COMPILED_NOT_RENDERED routes='+str(len(out['routes'])))
    print('REQUIRES_VISUAL_REVIEW')
    return 0
if __name__=='__main__':raise SystemExit(main())
