"""Guard shared thresholds and the actual Blueprint data contract."""
import copy
import json
import unittest
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
def config(path):
    return yaml.safe_load((ROOT / path).read_text())

class RuleContractTests(unittest.TestCase):
    def test_lead_candidate_thresholds_stay_consistent(self):
        retrieval = config('core/reference_retrieval.yaml')
        policy = config('core/lead_reference_policy.yaml')
        self.assertEqual(retrieval['lead_candidate_thresholds'], policy['lead_candidate_thresholds'])
        self.assertEqual(retrieval['support_reference_max'], policy['support_reference_max'])
    def test_strong_lead_thresholds_stay_consistent(self):
        validity = config('core/lead_validity_gate.yaml')['strong_lead_thresholds']
        mode = config('core/strong_anchor_mode.yaml')['enable_when']
        for key, other in {'topology':'topology_match_min','medium_surface':'medium_surface_match_min',
                          'typography_DNA':'typography_DNA_match_min','palette_value_regime':'palette_value_match_min',
                          'overall':'overall_match_min'}.items():
            self.assertEqual(validity[key], mode[other])
    def test_template_threshold_uses_route_scale(self):
        risk = config('core/safe_template_penalty.yaml')['high_risk_combination']
        route = config(risk['concept_score_source'])
        self.assertEqual(risk['concept_score_max'], route['route_gate_weights']['concept_embodiment'])
        self.assertLessEqual(risk['concept_embodiment_below'], risk['concept_score_max'])
    def test_blueprint_example_and_required_sections(self):
        schema=json.loads((ROOT/'schemas/reference_blueprint.schema.json').read_text())
        validator=Draft202012Validator(schema)
        data=config('examples/reference_blueprint_example.yaml')
        validator.validate(data)
        for field in ('borrow','transform','do_not_copy','target_tolerance'):
            missing=copy.deepcopy(data); del missing[field]
            with self.assertRaises(ValidationError): validator.validate(missing)
