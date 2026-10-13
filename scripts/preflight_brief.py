#!/usr/bin/env python3
"""Offline brief preflight. Never invent event facts. Usage: python scripts/preflight_brief.py brief.json"""
import sys, json
from pathlib import Path

def get_value(fields,key):
    obj=fields.get(key,{})
    if isinstance(obj,dict):
        if obj.get('status') != 'confirmed': return None
        v=obj.get('value')
        return v if v not in (None,'','TBD','TBA','待定') else None
    return None

def assess(doc):
    fields=doc.get('fields',{})
    purpose=doc.get('poster_purpose','announcement')
    mode=doc.get('event_mode','offline')
    wants=doc.get('requirements',{})
    allow_tba=purpose=='teaser' and doc.get('explicit_tba_permission') is True
    missing=[]; warnings=[];defaults=[]
    if not get_value(fields,'title_zh') and not get_value(fields,'title_en'):
        missing.append('活动正式名称（中文或英文至少一个）')
    if not allow_tba and not (get_value(fields,'date_text') or get_value(fields,'date_start')):
        missing.append('活动日期')
    if mode in ('offline','hybrid') and not allow_tba and not get_value(fields,'venue_name'):
        missing.append('准确活动地点/场馆')
    if mode in ('online','hybrid') and not allow_tba and not get_value(fields,'online_url'):
        missing.append('线上参与/报名访问方式')
    if wants.get('ticket_price_required') and not get_value(fields,'ticket_price'):
        missing.append('票价（海报要求必须展示）')
    if wants.get('registration_qr_required') and not get_value(fields,'registration_url'):
        missing.append('预约/报名链接（供 QR 使用）')
    if wants.get('organizer_required') and not get_value(fields,'organizer'):
        missing.append('正式主办方名称')
    langs=doc.get('languages',['zh'])
    if 'en' in langs and not get_value(fields,'title_en'):
        warnings.append('英文标题缺正式确认：允许草拟排版，但成稿前需确认专名译法')
    if not get_value(fields,'logo'):
        defaults.append('未提供 logo：可用文字署名或省略，不自动生成官方标识')
    if not get_value(fields,'hero_asset'):
        defaults.append('未提供主视觉素材：可在授权范围内生成，不是阻断项')
    result={'status':'WAITING_FOR_USER' if missing else 'READY_BASELINE',
            'blocking_missing':missing,'confirmation_warnings':warnings,'nonblocking_defaults':defaults,
            'may_generate_hero':not missing,
            'suggested_question': ('为了制作正式海报，请补充：'+'；'.join(missing)+'。如果是预热海报，请明确允许日期/地点待公布。') if missing else None}
    return result

if __name__=='__main__':
    if len(sys.argv)<2:raise SystemExit('Usage: python preflight_brief.py brief.json')
    print(json.dumps(assess(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))
