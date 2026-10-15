#!/usr/bin/env python3
"""Advisory ranking over canonical S1–S8 production styles and independent anchor topology."""
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def recommend(p):
    families=read('libraries/styles/packs.json')['packs'];masters=read('libraries/layouts/templates.json')['layouts'];rules=read('libraries/matching_matrix.json')
    fs={f['id'] for f in families};ms={m['id'] for m in masters};constraints=p.get('constraints',{})
    unknown=[]
    for key,valid in [('allowed_style_ids',fs),('excluded_style_ids',fs),('allowed_layout_ids',ms),('excluded_layout_ids',ms)]:
        unknown += [x for x in constraints.get(key,[]) if x not in valid]
    unknown += [x for x in p.get('reference_assessments',{}) if x not in fs]
    if unknown:return {'status':'needs_taxonomy_migration','unknown_ids':sorted(set(unknown)),'migration_guide':'libraries/taxonomy_migration.json','candidates':[],'checkpoint_approved':False}
    c=p['communication']
    if c['density'] not in ('low','medium','high'):raise ValueError('invalid density')
    evidence=p.get('evidence',{});warnings=[];rejected=[]
    if 'hero_form' in c:warnings.append('旧hero_form混合媒介与数量，未用于新骨架分类；请改用parameters与主锚观察证据')
    def number(v,label):
        if type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1:raise ValueError(label+' must be finite in [0,1]')
        return v
    def confidence(key):
        e=evidence.get(key,{});v=number(e.get('confidence',0),'confidence')
        if not e.get('source') or v<0.5:warnings.append('低置信或缺证据: '+key);return 0
        return v
    def affinity(values,allowed,field):
        pairs=[(x,confidence(field+'.'+x)) for x in dict.fromkeys(values)];denom=sum(v for _,v in pairs)
        return sum(v for x,v in pairs if x in allowed)/denom if denom else 0
    rows=[]
    if constraints.get('allowed_style_ids')==[]:return {'status':'needs_custom_style','candidates':[],'checkpoint_approved':False}
    if constraints.get('allowed_layout_ids')==[]:return {'status':'needs_custom_layout','candidates':[],'checkpoint_approved':False}
    for f in families:
        fid=f['id']
        if fid in constraints.get('excluded_style_ids',[]) or ('allowed_style_ids' in constraints and fid not in constraints['allowed_style_ids']):continue
        if f.get('material_requirements',{}).get('reliable_scene_photo'):
            scene=p.get('materials',{}).get('scene_photo',{})
            if scene.get('verified') is not True or not scene.get('source') or not scene.get('path') or not Path(scene['path']).is_file():
                rejected.append({'style':fid,'reason':'S2缺少已看图确认且路径有效的可靠实景照片；不得伪造现场'});continue
        ref=p.get('reference_assessments',{}).get(fid,{})
        if p.get('reference_constraint') and (ref.get('compatible') is not True or not ref.get('evidence')):
            rejected.append({'style':fid,'reason':'明确参考缺兼容证据或不兼容'});continue
        channel=p.get('channel_assessments',{}).get(fid,{})
        C=number(channel['score'],'channel score') if channel.get('evidence') and 'score' in channel else 0
        if not channel.get('evidence'):warnings.append('渠道适配未评估: '+fid+'，不凭风格名称臆测印刷/屏幕适配')
        dims={'T':affinity(p.get('theme_tags',[]),f['theme_tags'],'theme_tags'),'M':affinity([p['mood']['primary']]+p['mood'].get('secondary',[]),f['moods'],'mood'),'A':affinity(p.get('audience',[]),f['audiences'],'audience'),'C':C,'R':number(ref.get('score',0),'reference score')}
        weights=dict(rules['weights'])
        if not p.get('reference_constraint'):weights.pop('R')
        base=sum(dims[k]*v for k,v in weights.items())/sum(weights.values())
        for m in masters:
            mid=m['id']
            if mid in constraints.get('excluded_layout_ids',[]) or ('allowed_layout_ids' in constraints and mid not in constraints['allowed_layout_ids']):continue
            capacity=p.get('layout_assessments',{}).get(mid,{})
            if capacity.get('capacity_ok') is False:
                rejected.append({'style':fid,'layout':mid,'reason':'本次容量评估明确不满足'});continue
            if c['density'] not in m['density_natural'] and (capacity.get('capacity_ok') is not True or not capacity.get('evidence')):
                rejected.append({'style':fid,'layout':mid,'reason':'非自然密度缺容量证据，不能视作风格不兼容'});continue
            hist=[]
            for h in p.get('history',[]):
                if h.get('style') in fs and h.get('layout') in ms:hist.append(h)
                else:warnings.append('旧或未知分类历史未参与重复惩罚；请按迁移说明人工拆轴')
            pen=rules['repeat_penalty'];penalty=min(pen['maximum'],sum(pen['per_same_style'] for h in hist if h.get('style')==fid)+sum(pen['per_same_layout'] for h in hist if h.get('layout')==mid))
            bonus=rules['topology_preference_bonus'] if mid in f['topology_tendency_reasons'] else 0
            rows.append({'style':fid,'style_name':f['name'],'guide':f['guide'],'recommendation_evidence_required':'每候选2条适配证据+1条代价，不能只依据标签分','layout':mid,'layout_name':m['name'],'score':round(base+bonus-penalty,5),'components':dims,'topology_preference_bonus':bonus,'preference_reason':f['topology_tendency_reasons'][mid] if bonus else '该跨轴组合仍可行，不因无常见倾向而排除','repeat_penalty':penalty,'capacity_basis':'自然密度（仍须实际试排）' if c['density'] in m['density_natural'] else capacity['evidence'],'reference_ids':[x['id'] for x in f['reference_pool']],'reference_status':'历史候选池不等于S1–S8图库已审定','parameters':p.get('parameters',{}),'parameters_to_choose':'libraries/design_parameters.json','checkpoint_approved':False})
    if rows and not constraints.get('allowed_style_ids') and not any(any(v>0 for v in row['components'].values()) for row in rows):
        return {'status':'needs_design_evidence','candidates':[],'warnings':sorted(set(warnings))+['没有可用的适配证据；不得按ID或常见倾向回退到最安全模板'],'checkpoint_approved':False}
    rows.sort(key=lambda x:(-x['score'],x['style'],x['layout']))
    return {'status':'awaiting_style_confirmation' if rows else 'needs_constraints_review','candidates':rows,'rejected':rejected,'warnings':sorted(set(warnings)),'weight_status':rules['weight_status'],'classification_limits':'标签适配分不等于风格认定；按八风格详细指南看图核验，骨架独立选择','checkpoint_approved':False}
def main():
    a=argparse.ArgumentParser();a.add_argument('--profile',required=True);a.add_argument('--out');args=a.parse_args();data=json.dumps(recommend(json.loads(Path(args.profile).read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)
    if args.out:Path(args.out).write_text(data,encoding='utf-8')
    print(data)
if __name__=='__main__':main()
