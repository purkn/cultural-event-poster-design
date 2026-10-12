#!/usr/bin/env python3
"""v0.19 final-render text-over-image gate and conservative repair.

Evaluates actual SVG raster against independently rendered pre-text scene;
never estimates from whole-image luminance. The output is a measurable
production audit, NOT a substitute for artistic/subject saliency review.
"""
import argparse
import copy
import io
import hashlib
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image
try:
    import cairosvg
except ImportError:
    cairosvg=None
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_poster_svg import generate, LayoutError, SVG, SVG_NS

DEFAULTS={
    'contrast_body':4.5, 'contrast_large':3.0,
    'min_local_pass_fraction':0.92, 'min_local_q10_multiplier':1.0,
    'complex_edge_density':0.18, 'complex_luma_std':0.205,
    'min_h0_thumbnail_font_px':12.0, 'min_key_thumbnail_font_px':7.5,
    'thumbnail_scale':0.25, 'max_repair_rounds':2,
    'max_relocation_fraction':0.065,
    'max_tint_opacity':0.16, 'max_tint_area_ratio':0.10,
}

def policy_for(plan):
    overrides=plan.get('readability_policy',{})
    floor=['contrast_body','contrast_large','min_local_pass_fraction','min_local_q10_multiplier',
           'min_h0_thumbnail_font_px','min_key_thumbnail_font_px']
    ceiling=['complex_edge_density','complex_luma_std','max_tint_opacity','max_tint_area_ratio',
             'max_repair_rounds']
    for k in floor:
        if k in overrides and float(overrides[k]) < DEFAULTS[k]:
            raise ValueError('POLICY_WEAKENING_FORBIDDEN:'+k)
    for k in ceiling:
        if k in overrides and float(overrides[k]) > DEFAULTS[k]:
            raise ValueError('POLICY_WEAKENING_FORBIDDEN:'+k)
    if float(overrides.get('thumbnail_scale',0.25))>0.25:
        raise ValueError('POLICY_WEAKENING_FORBIDDEN:thumbnail_scale')
    if float(overrides.get('max_relocation_fraction',0.065))>0.10:
        raise ValueError('POLICY_WEAKENING_FORBIDDEN:max_relocation_fraction')
    return {**DEFAULTS,**overrides}

def to_rgb_array(im):
    return np.asarray(im.convert('RGB'),dtype=np.float32)/255.0

def luminosity(rgb):
    lin=np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)
    return 0.2126*lin[...,0]+0.7152*lin[...,1]+0.0722*lin[...,2]

def wcag_ratio(fore,back):
    a=luminosity(fore);b=luminosity(back)
    return (np.maximum(a,b)+0.05)/(np.minimum(a,b)+0.05)

def render(root,W,H):
    if cairosvg is None:raise RuntimeError('CAIROSVG_REQUIRED')
    data=ET.tostring(root,encoding='utf-8')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=data,output_width=W,output_height=H))).convert('RGBA')

def separate_layers(svgpath):
    root=ET.parse(svgpath).getroot()
    w=int(float(root.attrib['width']));h=int(float(root.attrib['height']))
    texts=[n for n in list(root) if n.tag==SVG('text') or n.attrib.get('id')=='h0-custom-editable-paths']
    if not texts:raise RuntimeError('NO_EDITABLE_TEXT_LAYERS')
    background=copy.deepcopy(root)
    for n in list(background):
        if n.tag==SVG('text') or n.attrib.get('id')=='h0-custom-editable-paths':background.remove(n)
    before=render(background,w,h).convert('RGB')
    final=render(root,w,h).convert('RGB')
    glyphs={}
    for n in texts:
        only=copy.deepcopy(root)
        for m in list(only):
            if m.tag not in (SVG('defs'), SVG('title'),SVG('desc')):only.remove(m)
        only.append(copy.deepcopy(n))
        glyphs['h0' if n.attrib.get('id')=='h0-custom-editable-paths' else n.attrib.get('id','h0')]=render(only,w,h)
    return final,before,glyphs

def compute_one(block,fg,bg,final,pol,protected):
    role=block.get('role','h0' if block['id']=='h0' else 'body')
    important=role in ('h0','key','critical','cta') or bool(block.get('critical',False))
    alpha=np.asarray(fg,dtype=np.uint8)[...,3].astype(np.float32)/255.
    yy,xx=np.where(alpha>0.075)
    if len(xx)<3:
        return {'id':block['id'],'text':block['text'],'role':role,'status':'FAIL', 'reasons':['TEXT_NOT_RENDERED']}
    x0,y0,x1,y1=int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)
    core=alpha[y0:y1,x0:x1]>0.62
    if core.sum()<3:core=alpha[y0:y1,x0:x1]>0.2
    fore=to_rgb_array(fg)[y0:y1,x0:x1][core]
    bkg=to_rgb_array(bg)[y0:y1,x0:x1][core]
    ratios=wcag_ratio(fore,bkg)
    sz=float(block.get('font_size',max(24, y1-y0)))
    large=sz>=24 or (sz>=19 and str(block.get('font_weight','')).lower() in ('bold','600','700','800','900'))
    thresh=float(pol['contrast_large'] if large else pol['contrast_body'])
    q10=float(np.percentile(ratios,10))
    fraction=float(np.mean(ratios>=thresh))
    # Complexity uses the local text bounding region, not poster average.
    px=10; xa=max(x0-px,0);xb=min(x1+px,bg.width);ya=max(y0-px,0);yb=min(y1+px,bg.height)
    region=to_rgb_array(bg)[ya:yb,xa:xb]
    lum=luminosity(region)
    std=float(lum.std())
    grads=(np.abs(np.diff(lum,axis=1))>0.11).mean() if lum.shape[1]>1 else 0.0
    grads2=(np.abs(np.diff(lum,axis=0))>0.11).mean() if lum.shape[0]>1 else 0.0
    edges=float((grads+grads2)/2)
    comp=edges>pol['complex_edge_density'] or std>pol['complex_luma_std']
    collisions=[]
    for r in protected:
        rx,ry,rw,rh=[float(r[k]) for k in ('x','y','width','height')]
        ow=max(0,min(x1,rx+rw)-max(x0,rx));oh=max(0,min(y1,ry+rh)-max(y0,ry))
        area=(x1-x0)*(y1-y0)
        if area and ow*oh/area>0.04 and r.get('importance','critical')=='critical':
            collisions.append(r.get('id','unnamed-subject'))
    # Downscale the *actual composited* picture; legibility metrics here
    # are an engineering proxy, not a true viewer acuity test.
    factor=float(pol['thumbnail_scale'])
    ws=max(1,round(bg.width*factor));hs=max(1,round(bg.height*factor))
    fg_small=fg.resize((ws,hs),Image.Resampling.LANCZOS)
    bg_small=bg.resize((ws,hs),Image.Resampling.LANCZOS)
    fin_small=final.resize((ws,hs),Image.Resampling.LANCZOS)
    a_small=np.asarray(fg_small)[...,3].astype(np.float32)/255.
    sampled=a_small>0.20
    if sampled.any():
        sb=luminosity(to_rgb_array(bg_small));sf=luminosity(to_rgb_array(fin_small))
        thumbnail_signal=float(np.percentile(np.abs(sf[sampled]-sb[sampled]),50))
    else:thumbnail_signal=0.
    font_small=sz*factor
    reasons=[];warnings=[]
    if fraction<pol['min_local_pass_fraction'] or q10<thresh*pol['min_local_q10_multiplier']:
        reasons.append('LOCAL_CONTRAST_FAIL')
    if collisions:reasons.append('IMPORTANT_SUBJECT_OVERLAP')
    if comp:
        # Complexity alone needs an informed style review unless important key text
        # is only marginally distinguishable from a busy background.
        if important and (q10<thresh*1.35 or fraction<0.985):
            reasons.append('COMPLEX_BACKGROUND_WEAK_TEXT')
        else:warnings.append('HIGH_BACKGROUND_COMPLEXITY_REVIEW')
    if important and font_small<(pol['min_h0_thumbnail_font_px'] if role=='h0' else pol['min_key_thumbnail_font_px']):
        reasons.append('KEY_TEXT_TOO_SMALL_AT_THUMBNAIL')
    if important and thumbnail_signal<0.095:
        reasons.append('LOW_THUMBNAIL_VISIBILITY')
    if not important and font_small<5.5:warnings.append('BODY_TEXT_SMALL_AT_THUMBNAIL')
    return {
        'id':block['id'],'text':block['text'],'role':role,'status':'FAIL' if reasons else ('REVIEW' if warnings else 'PASS'),
        'bbox_px':[x0,y0,x1-x0,y1-y0],
        'contrast_threshold':thresh,'contrast_q10':round(q10,3),'contrast_min':round(float(np.min(ratios)),3),
        'contrast_pass_fraction':round(fraction,4),
        'luminance_std':round(std,4),'edge_density':round(edges,4),
        'high_background_complexity':bool(comp),
        'thumbnail_font_px':round(font_small,2),'thumbnail_signal':round(thumbnail_signal,3),
        'protected_overlap':collisions,'reasons':reasons,'warnings':warnings}

def audit(plan,svgfile,save_dir=None):
    pol=policy_for(plan)
    final,before,glyphs=separate_layers(svgfile)
    boxes=[{'id':plan['h0'].get('id','h0'), **plan['h0'], 'role':'h0'}]+[
        {'role':'body',**b} for b in plan.get('text_blocks',[])]
    findings=[]
    for b in boxes:
        ident=b['id']
        if ident not in glyphs:
            findings.append({'id':ident,'text':b.get('text'), 'status':'FAIL','reasons':['TEXT_LAYER_MISSING']})
        else:findings.append(compute_one(b,glyphs[ident],before,final,pol,plan.get('protected_regions',[])))
    if save_dir:
        d=Path(save_dir);d.mkdir(parents=True,exist_ok=True)
        final.save(d/'final_render.png');before.save(d/'pre_text_background.png')
    return {'overall':'FAIL' if any(f['status']=='FAIL' for f in findings) else
             ('REVIEW_REQUIRED' if any(f['status']=='REVIEW' for f in findings) else 'MEASURABLE_PASS'),
            'renderer':'CairoSVG','note':'Automated proxy; subjective typography and unannotated subject saliency still require visual approval.',
            'protected_regions_supplied':bool(plan.get('protected_regions')),
            'final_delivery_allowed':False, 'findings':findings}

def evaluate_plan(plan,workdir,prefix):
    svg=workdir/(prefix+'.svg')
    generate(plan,svg)
    return audit(plan,svg),svg

def try_candidates(plan,fail,workdir,roundnum):
    pol=policy_for(plan)
    fid=fail['id']
    box=plan['h0'] if plan['h0'].get('id','h0')==fid else next((b for b in plan.get('text_blocks',[]) if b.get('id')==fid),None)
    if box is None or box.get('mode')=='CUSTOM_GLYPH':return None
    def check(p,desc):
        try:
            report,_=evaluate_plan(p,workdir,'candidate')
        except (LayoutError, OSError,RuntimeError,ValueError):return None
        item=next((i for i in report['findings'] if i['id']==fid),None)
        if not item:return None
        # No regression for already passing text. Every repair must protect other text.
        old_fails={i['id'] for i in original_report['findings'] if i['status']=='FAIL'}
        new_fails={i['id'] for i in report['findings'] if i['status']=='FAIL'}
        if new_fails-old_fails:return None
        if item['status']!='FAIL' and fid not in new_fails:return (p,desc,report)
        return None
    # Closure compares against the current audit snapshot, never a fabricated score.
    original_report,_=evaluate_plan(plan,workdir,'base')
    if not box.get('lock_position',False):
        max_dx=float(pol['max_relocation_fraction'])*plan['canvas']['width']
        max_dy=float(pol['max_relocation_fraction'])*plan['canvas']['height']
        steps=[(-32,0),(32,0),(0,-32),(0,32),(-64,0),(64,0),(0,-64),(0,64),(-32,-32),(32,32)]
        for dx,dy in steps:
            if abs(dx)>max_dx or abs(dy)>max_dy:continue
            p=copy.deepcopy(plan)
            b=p['h0'] if p['h0'].get('id','h0')==fid else next(x for x in p['text_blocks'] if x.get('id')==fid)
            b['x']=box['x']+dx;b['y']=box['y']+dy
            result=check(p,{'type':'relocate','target':fid,'delta':[dx,dy]})
            if result:return result
    # Color selection must come from the style-approved palette, not automatic black/white.
    allowed=box.get('approved_text_colors',plan.get('readability_policy',{}).get('approved_text_colors',[]))
    for color in allowed:
        if color==box.get('fill'):continue
        p=copy.deepcopy(plan)
        b=p['h0'] if p['h0'].get('id','h0')==fid else next(x for x in p['text_blocks'] if x.get('id')==fid)
        b['fill']=color
        result=check(p,{'type':'approved_color','target':fid,'from':box['fill'],'to':color})
        if result:return result
    # Optional safe-area-limited tint. Not a full-page black overlay.
    policy=plan.get('readability_policy',{})
    if 'local_tint' in policy.get('allowed_treatments',[]) and fail.get('bbox_px'):
        x,y,w,h=fail['bbox_px']; pad=12
        for color in policy.get('approved_tint_colors',[]):
            p=copy.deepcopy(plan)
            p.setdefault('local_readability_treatments',[]).append({
                'x':max(0,x-pad),'y':max(0,y-pad),
                'width':min(plan['canvas']['width']-max(0,x-pad),w+2*pad),
                'height':min(plan['canvas']['height']-max(0,y-pad),h+2*pad),
                'opacity':min(0.16,float(policy.get('max_tint_opacity',0.16))),
                'fill':color})
            # Strict fail closed if a treatment covers important subject region.
            tr=p['local_readability_treatments'][-1]
            collision=False
            for r in p.get('protected_regions',[]):
                if r.get('importance','critical')!='critical':continue
                ow=max(0,min(tr['x']+tr['width'],r['x']+r['width'])-max(tr['x'],r['x']))
                oh=max(0,min(tr['y']+tr['height'],r['y']+r['height'])-max(tr['y'],r['y']))
                if ow*oh>0:collision=True
            if collision:continue
            result=check(p,{'type':'limited_local_tint','target':fid,'color':color,'opacity':tr['opacity']})
            if result:return result
    return None

def run(plan_path,outdir,max_rounds=None,visual_review_file=None):
    plan_path=Path(plan_path).resolve();outdir=Path(outdir).resolve();outdir.mkdir(parents=True,exist_ok=True)
    plan=json.loads(plan_path.read_text(encoding='utf8'))
    # Resolve user image paths relative to plan, not cwd (portable tests).
    if plan.get('hero') and not Path(plan['hero']['file']).is_absolute():
        plan['hero']['file']=str((plan_path.parent/plan['hero']['file']).resolve())
    original=copy.deepcopy(plan);rounds=[]
    policy_for(plan)
    cap=int(max_rounds if max_rounds is not None else plan.get('readability_policy',{}).get('max_repair_rounds',2))
    if cap<0 or cap>2:raise ValueError('MAX_REPAIR_ROUNDS_MUST_BE_0_TO_2')
    for r in range(cap+1):
        result,svg=evaluate_plan(plan,outdir,f'round_{r}')
        rows=[f for f in result['findings'] if f['status']=='FAIL']
        rounds.append({'round':r,'overall':result['overall'], 'findings':result['findings']})
        if not rows or r==cap:break
        done=False
        for fail in rows:
            updated=try_candidates(plan,fail,outdir,r)
            if updated:
                plan,change,_=updated
                rounds[-1].setdefault('repairs',[]).append(change)
                done=True;break
        if not done:break
    # FINAL re-render mandatory after corrections, then audit exact that asset.
    svg=outdir/'poster_final_review.svg'
    generate(plan,svg)
    result=audit(plan,svg,save_dir=outdir)
    deliverable=result['overall']!='FAIL'
    image_digest=hashlib.sha256((outdir/'final_render.png').read_bytes()).hexdigest()
    approval='PENDING'
    if visual_review_file:
        evidence=json.loads(Path(visual_review_file).read_text(encoding='utf8'))
        required={'text_over_subject','font_personality','type_hierarchy','thumbnail_readability','hero_visual_integrity'}
        if (evidence.get('render_sha256')==image_digest and evidence.get('decision')=='PASS'
            and isinstance(evidence.get('reviewer'),str) and evidence['reviewer'].strip()
            and isinstance(evidence.get('observations'),dict)
            and set(evidence['observations'])>=required
            and all(isinstance(evidence['observations'][k],str) and len(evidence['observations'][k])>=12 for k in required)):
            approval='PASS'
        else:approval='REJECTED_INVALID_OR_STALE'
    result.update({'final_delivery_allowed': bool(deliverable and approval=='PASS'),
                   'visual_review_status':approval,
                   'render_sha256':image_digest,
                   'technical_readability_gate':'PASS' if deliverable else 'FAIL',
                   'visual_approval_required':True,
                   'auto_repair_rounds_used':len(rounds)-1,
                   'change_log':[i for round_ in rounds for i in round_.get('repairs',[])],
                   'repair_history':rounds,
                   'must_escalate_layout':not deliverable})
    (outdir/'readability_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    (outdir/'poster_plan_review.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
    return result

def main():
    parser=argparse.ArgumentParser(description='Final SVG contrast/complexity/subject gate and constrained repair')
    parser.add_argument('plan');parser.add_argument('--out-dir',required=True);parser.add_argument('--max-rounds',type=int)
    parser.add_argument('--visual-review',help='JSON review of exact final PNG digest and five visual dimensions')
    args=parser.parse_args()
    try:
        result=run(args.plan,args.out_dir,args.max_rounds,args.visual_review)
        print(json.dumps({'technical_readability_gate':result['technical_readability_gate'],
                          'final_delivery_allowed':result['final_delivery_allowed'],
                          'must_escalate_layout':result['must_escalate_layout'],
                          'report':str(Path(args.out_dir)/'readability_report.json')},ensure_ascii=False))
        sys.exit(0 if result['technical_readability_gate']=='PASS' else 3)
    except (LayoutError,RuntimeError,ValueError,KeyError,OSError) as exc:
        print('READABILITY_AUDIT_ERROR:'+str(exc),file=sys.stderr);sys.exit(2)
if __name__=='__main__':main()
