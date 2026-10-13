import copy
import tempfile
import unittest
from pathlib import Path
from review_fixtures import review_fixture
from poster_review import assess_review, review_config


class PosterReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('final.png', 'thumb.png', 'plan.json'):
            (self.root / name).write_bytes(name.encode())
        self.review = review_fixture(self.root, self.root / 'final.png', self.root / 'thumb.png', self.root / 'plan.json')
        self.render = self.review['render_sha256']
        self.thumb = self.review['artifacts']['thumbnail']['sha256']

    def assess(self, review=None):
        return assess_review(self.review if review is None else review, self.render, self.thumb, self.root)

    def test_complete_review_passes_and_computes_scores(self):
        result = self.assess()
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['design_score'], 100)
        self.assertEqual(result['production_score'], 100)

    def test_old_five_observation_review_no_longer_grants_pass(self):
        old = {k: self.review[k] for k in ('render_sha256', 'decision', 'reviewer', 'observations')}
        self.assertEqual(self.assess(old)['status'], 'REJECTED_INCOMPLETE')

    def test_technical_quality_cannot_compensate_design(self):
        for row in self.review['design_scores'].values():
            row['score'] *= 0.8
        self.assertIn('BELOW_PASS_THRESHOLD:design', self.assess()['issues'])

    def test_design_cannot_compensate_production(self):
        for row in self.review['production_scores'].values():
            row['score'] *= 0.84
        self.assertIn('BELOW_PASS_THRESHOLD:production', self.assess()['issues'])

    def test_exact_thresholds_are_valid(self):
        for axis, ratio in [('design', .82), ('production', .85)]:
            for row in self.review[axis + '_scores'].values():
                row['score'] *= ratio
        self.assertEqual(self.assess()['status'], 'PASS')

    def test_invalid_numbers_rejected(self):
        for number in (True, float('nan'), float('inf'), -1, 200):
            review = copy.deepcopy(self.review)
            next(iter(review['design_scores'].values()))['score'] = number
            self.assertNotEqual(self.assess(review)['status'], 'PASS')

    def test_missing_dimension_and_invalid_evidence_reference_rejected(self):
        key = next(iter(self.review['design_scores']))
        review = copy.deepcopy(self.review)
        del review['design_scores'][key]
        self.assertNotEqual(self.assess(review)['status'], 'PASS')
        self.review['design_scores'][key]['artifact_refs'] = ['imaginary-file']
        self.assertNotEqual(self.assess()['status'], 'PASS')

    def test_changed_reference_invalidates_review(self):
        Path(self.review['artifacts']['reference_comparison']['path']).write_text('changed')
        self.assertIn('ARTIFACT_SHA256_MISMATCH:reference_comparison', self.assess()['issues'])

    def test_poster_plan_must_match_current_rendered_plan(self):
        result = assess_review(self.review, self.render, self.thumb, self.root,
                               poster_plan_sha256='old-plan-hash')
        self.assertIn('ARTIFACT_NOT_CURRENT_POSTER_PLAN', result['issues'])
        self.assertNotEqual(result['status'], 'PASS')

    def test_changed_thumbnail_invalidates_review(self):
        self.thumb = 'not-current-thumbnail'
        self.assertIn('ARTIFACT_NOT_CURRENT_THUMBNAIL', self.assess()['issues'])

    def test_contextual_pattern_exception_requires_reason(self):
        key = next(iter(self.review['anti_default']))
        self.review['anti_default'][key]['status'] = 'JUSTIFIED'
        self.assertNotEqual(self.assess()['status'], 'PASS')
        self.review['anti_default'][key]['reason'] = 'The supplied Lead uses this device to frame the event title.'
        self.assertEqual(self.assess()['status'], 'PASS')

    def test_fail_preflight_blocks_even_perfect_scores(self):
        key = next(iter(self.review['preflight']))
        self.review['preflight'][key]['status'] = 'FAIL'
        self.assertIn('CHECK_UNRESOLVED:' + key, self.assess()['issues'])

    def test_issue_needs_repair_and_current_render_recheck(self):
        issue = {'area': 'H0', 'evidence': 'Title competes with the main subject.',
                 'repair_action': 'Move title to the reserved reading area.', 'status': 'OPEN'}
        self.review['issues'] = [issue]
        self.assertNotEqual(self.assess()['status'], 'PASS')
        issue['status'] = 'RESOLVED'
        issue['recheck_evidence'] = 'Inspected the corrected title location and thumbnail.'
        issue['rechecked_render_sha256'] = 'old-hash'
        self.assertNotEqual(self.assess()['status'], 'PASS')
        issue['rechecked_render_sha256'] = self.render
        self.assertEqual(self.assess()['status'], 'PASS')

    def test_relative_artifact_paths_are_based_on_review_directory(self):
        for artifact in self.review['artifacts'].values():
            artifact['path'] = Path(artifact['path']).name
        self.assertEqual(self.assess()['status'], 'PASS')

    def test_nonobject_and_invalid_status_do_not_crash_or_pass(self):
        self.assertNotEqual(self.assess([])['status'], 'PASS')
        self.review['decision'] = []
        next(iter(self.review['preflight'].values()))['status'] = []
        self.assertNotEqual(self.assess()['status'], 'PASS')

    def test_rework_decision_cannot_grant_pass(self):
        self.review['decision'] = 'REWORK'
        self.assertEqual(self.assess()['status'], 'REWORK')

    def test_policy_uses_only_authoritative_score_table(self):
        policy, scoring = review_config()
        self.assertEqual(policy['score_source'], 'core/design_quality_scores.yaml')
        self.assertNotIn('pass_min', policy)
        self.assertEqual(sum(scoring['design_dimensions'].values()), scoring['design_score_total'])
        self.assertEqual(sum(scoring['production_dimensions'].values()), scoring['production_score_total'])
