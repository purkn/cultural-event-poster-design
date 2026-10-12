#!/usr/bin/env python3
"""Offline LoRA candidate eligibility. Never downloads or loads weights."""
import json,argparse
from pathlib import Path

def assess(backend,candidate,commercial=False):
    issues=[]
    support=backend.get('supports_external_lora')
    if support is not True:
        return {'status':'SKIP_NO_BACKEND','issues':['Backend external LoRA support not explicitly confirmed'],'can_propose_download':False}
    for key in ('base_model_family','base_model_id'):
        b=backend.get(key);c=candidate.get(key)
        if not b or not c or b!=c:issues.append(f'Base compatibility mismatch/unknown: {key}')
    if not candidate.get('revision'):issues.append('Missing pinned model revision')
    if not candidate.get('license'):issues.append('License missing/unknown')
    if candidate.get('license_verified') is not True or not candidate.get('license_evidence_url'):issues.append('License verification evidence missing')
    if candidate.get('output_use_allowed') is not True:issues.append('Output-use permission not established')
    if candidate.get('source_verified') is not True:issues.append('Source not verified')
    if candidate.get('visual_previews_verified') is not True:issues.append('Visual previews not reviewed')
    if not str(candidate.get('weight_filename','')).endswith('.safetensors'):issues.append('Only safetensors allowed')
    size=candidate.get('size_mb')
    if not isinstance(size,(int,float)) or size<=0:issues.append('Weight size unknown')
    if commercial and candidate.get('commercial_output_allowed') is not True:
        issues.append('Commercial output use permission not established')
    if not issues:
        return {'status':'REQUEST_USER_APPROVAL','issues':[], 'can_propose_download':True,'can_download_now':False}
    return {'status':'REJECT_UNVERIFIED','issues':issues,'can_propose_download':False,'can_download_now':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--backend',required=True);ap.add_argument('--candidate',required=True);ap.add_argument('--commercial',action='store_true');args=ap.parse_args()
    print(json.dumps(assess(json.loads(Path(args.backend).read_text()), json.loads(Path(args.candidate).read_text()),args.commercial),ensure_ascii=False,indent=2))
