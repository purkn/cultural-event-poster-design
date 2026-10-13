"""Synthetic review data for gate tests; no aesthetic PASS claim."""
import hashlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from poster_review import review_config


def review_fixture(folder, render, thumbnail, plan):
    policy, scores = review_config()
    paths = {'final_render': render, 'thumbnail': thumbnail, 'poster_plan': plan}
    for role in policy['required_artifacts']:
        if role not in paths:
            paths[role] = folder / (role + '.txt')
            paths[role].write_text('Synthetic fixture only: ' + role)
    review = {
        'render_sha256': hashlib.sha256(render.read_bytes()).hexdigest(),
        'decision': 'PASS', 'reviewer': 'synthetic-test-reviewer',
        'design_read': {key: 'Synthetic test context: ' + key for key in policy['required_design_read']},
        'observations': {key: 'Synthetic observation for gate testing: ' + key for key in policy['required_observations']},
        'artifacts': {role: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                      for role, path in paths.items()},
        'preflight': {key: {'status': 'PASS', 'evidence': 'Synthetic checked evidence: ' + key}
                      for key in policy['preflight_checks']},
        'anti_default': {key: {'status': 'ABSENT', 'evidence': 'Synthetic absence observation: ' + key}
                         for key in policy['anti_default_checks']},
        'issues': [],
    }
    for axis in ('design', 'production'):
        review[axis + '_scores'] = {
            key: {'score': maximum, 'evidence': 'Synthetic rubric evidence: ' + key,
                  'artifact_refs': ['final_render']} for key, maximum in scores[axis + '_dimensions'].items()}
    return review
