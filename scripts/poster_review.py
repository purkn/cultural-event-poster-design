#!/usr/bin/env python3
"""Validate render-bound review evidence, scoring and unresolved issues.

This checks file integrity and review structure, not whether a human/agent
really viewed an image or whether its aesthetic judgement is correct.
"""
import hashlib
import json
import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def review_config(root=ROOT):
    policy = yaml.safe_load((root / 'core/universal_poster_critic.yaml').read_text())
    scores = yaml.safe_load((root / policy['score_source']).read_text())
    return policy, scores


def text_present(value):
    return (isinstance(value, str) and bool(value.strip())
            and not value.strip().upper().startswith(('REPLACE_', 'TODO', 'PENDING')))


def assess_review(evidence, render_sha256, thumbnail_sha256, base_dir, root=ROOT, poster_plan_sha256=None):
    """Return a verdict; never infer visual quality from pixels or filename."""
    policy, scoring = review_config(root)
    errors = []
    if not isinstance(evidence, dict):
        return {'status': 'REJECTED_INCOMPLETE', 'issues': ['REVIEW_MUST_BE_OBJECT']}
    if evidence.get('render_sha256') != render_sha256:
        return {'status': 'REJECTED_INVALID_OR_STALE', 'issues': ['RENDER_SHA256_MISMATCH']}
    if not text_present(evidence.get('reviewer')):
        errors.append('REVIEWER_REQUIRED')
    for section, keys in [('design_read', policy['required_design_read']),
                          ('observations', policy['required_observations'])]:
        data = evidence.get(section)
        if not isinstance(data, dict):
            errors.append('MISSING_SECTION:' + section)
            continue
        for key in keys:
            if not text_present(data.get(key)):
                errors.append('MISSING_EVIDENCE:' + section + '.' + key)
    artifacts = evidence.get('artifacts')
    valid_roles = set()
    if not isinstance(artifacts, dict):
        errors.append('ARTIFACTS_REQUIRED')
        artifacts = {}
    roles = list(policy['required_artifacts']) + sorted(set(artifacts) - set(policy['required_artifacts']))
    for role in roles:
        asset = artifacts.get(role)
        if not isinstance(asset, dict) or not text_present(asset.get('path')):
            errors.append('ARTIFACT_REQUIRED:' + role)
            continue
        path = Path(asset['path'])
        if not path.is_absolute():
            path = Path(base_dir) / path
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            errors.append('ARTIFACT_UNREADABLE:' + role)
            continue
        if asset.get('sha256') != digest:
            errors.append('ARTIFACT_SHA256_MISMATCH:' + role)
            continue
        if role == 'final_render' and digest != render_sha256:
            errors.append('ARTIFACT_NOT_CURRENT_RENDER')
            continue
        if role == 'thumbnail' and digest != thumbnail_sha256:
            errors.append('ARTIFACT_NOT_CURRENT_THUMBNAIL')
            continue
        if role == 'poster_plan' and poster_plan_sha256 is not None and digest != poster_plan_sha256:
            errors.append('ARTIFACT_NOT_CURRENT_POSTER_PLAN')
            continue
        valid_roles.add(role)
    for section, keys, statuses in [
            ('preflight', policy['preflight_checks'], {'PASS'}),
            ('anti_default', policy['anti_default_checks'], {'ABSENT', 'JUSTIFIED'})]:
        checks = evidence.get(section)
        if not isinstance(checks, dict):
            errors.append('MISSING_SECTION:' + section)
            continue
        for key in keys:
            check = checks.get(key)
            if not isinstance(check, dict) or not text_present(check.get('evidence')):
                errors.append('CHECK_EVIDENCE_REQUIRED:' + key)
            elif not isinstance(check.get('status'), str) or check.get('status') not in statuses:
                errors.append('CHECK_UNRESOLVED:' + key)
            elif check.get('status') == 'JUSTIFIED' and not text_present(check.get('reason')):
                errors.append('CONTEXT_JUSTIFICATION_REQUIRED:' + key)
    totals = {}
    for axis in ('design', 'production'):
        dimensions = scoring[axis + '_dimensions']
        rows = evidence.get(axis + '_scores')
        total = 0
        if not isinstance(rows, dict) or set(rows) != set(dimensions):
            errors.append('SCORE_DIMENSIONS_REQUIRED:' + axis)
            continue
        for key, maximum in dimensions.items():
            row = rows[key]
            if not isinstance(row, dict):
                errors.append('SCORE_ROW_REQUIRED:' + key)
                continue
            value = row.get('score')
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or not 0 <= value <= maximum):
                errors.append('SCORE_OUT_OF_RANGE:' + key)
            else:
                total += value
            if not text_present(row.get('evidence')):
                errors.append('SCORE_EVIDENCE_REQUIRED:' + key)
            refs = row.get('artifact_refs')
            if (not isinstance(refs, list) or not refs
                    or not all(isinstance(ref, str) and ref in valid_roles for ref in refs)):
                errors.append('SCORE_ARTIFACT_REFS_REQUIRED:' + key)
        totals[axis + '_score'] = round(total, 3)
        if total < scoring[axis + '_pass_min']:
            errors.append('BELOW_PASS_THRESHOLD:' + axis)
    issues = evidence.get('issues')
    if not isinstance(issues, list):
        errors.append('ISSUE_LIST_REQUIRED')
    else:
        for issue in issues:
            if not isinstance(issue, dict):
                errors.append('INVALID_ISSUE')
                continue
            if not all(text_present(issue.get(k)) for k in ('area', 'evidence', 'repair_action')):
                errors.append('ISSUE_DETAILS_REQUIRED')
            if issue.get('status') != 'RESOLVED':
                errors.append('UNRESOLVED_ISSUE:' + str(issue.get('area', 'unknown')))
            elif (issue.get('rechecked_render_sha256') != render_sha256
                  or not text_present(issue.get('recheck_evidence'))):
                errors.append('ISSUE_RECHECK_REQUIRED')
    decision = evidence.get('decision')
    if decision != 'PASS':
        errors.append('REVIEW_DECISION:' + str(decision))
    return {'status': ('PASS' if not errors else
                       'REWORK' if isinstance(decision, str) and decision in {'REWORK', 'REJECT'} else 'REJECTED_INCOMPLETE'),
            'issues': errors, **totals}
