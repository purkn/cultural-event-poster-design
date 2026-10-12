import sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
from preflight_brief import assess as brief_assess
from lora_gate import assess as lora_assess

def field(value):return {'value':value,'status':'confirmed' if value else 'missing','source':'user_text' if value else None}
class GateTests(unittest.TestCase):
    def test_missing_date_location_stops(self):
        r=brief_assess({'poster_purpose':'announcement','event_mode':'offline','fields':{'title_zh':field('文化节')}})
        self.assertEqual(r['status'],'WAITING_FOR_USER');self.assertFalse(r['may_find_lora']);self.assertEqual(len(r['blocking_missing']),2)
    def test_logo_optional(self):
        r=brief_assess({'poster_purpose':'announcement','event_mode':'offline','fields':{'title_zh':field('节'),'date_text':field('2026-12-02'),'venue_name':field('A馆')}})
        self.assertEqual(r['status'],'READY_BASELINE');self.assertTrue(r['may_generate_hero'])
    def test_teaser_requires_explicit_permission(self):
        d={'poster_purpose':'teaser','event_mode':'offline','fields':{'title_zh':field('文化节')}}
        self.assertEqual(brief_assess(d)['status'],'WAITING_FOR_USER')
        d['explicit_tba_permission']=True;self.assertEqual(brief_assess(d)['status'],'READY_BASELINE')
    def test_online_requires_url(self):
        r=brief_assess({'event_mode':'online','fields':{'title_zh':field('节'),'date_text':field('2026-12-02')}})
        self.assertEqual(r['status'],'WAITING_FOR_USER');self.assertTrue(any('线上' in x for x in r['blocking_missing']))
    def test_backend_unknown_skips(self):
        r=lora_assess({'supports_external_lora':None},{})
        self.assertEqual(r['status'],'SKIP_NO_BACKEND');self.assertFalse(r['can_propose_download'])
    def test_bad_license_fails(self):
        r=lora_assess({'supports_external_lora':True,'base_model_family':'SDXL','base_model_id':'A'},
           {'base_model_family':'SDXL','base_model_id':'A','revision':'rev','license':None,'source_verified':True,'visual_previews_verified':True,'weight_filename':'test.safetensors','size_mb':120})
        self.assertEqual(r['status'],'REJECT_UNVERIFIED')
    def test_license_name_alone_not_enough(self):
        r=lora_assess({'supports_external_lora':True,'base_model_family':'SDXL','base_model_id':'A'},
               {'base_model_family':'SDXL','base_model_id':'A','revision':'rev','license':'some-license','source_verified':True,'visual_previews_verified':True,'weight_filename':'test.safetensors','size_mb':120})
        self.assertEqual(r['status'],'REJECT_UNVERIFIED')
    def test_base_mismatch_fails(self):
        r=lora_assess({'supports_external_lora':True,'base_model_family':'SDXL','base_model_id':'A'},
           {'base_model_family':'FLUX','base_model_id':'B','revision':'rev','license':'openrail','source_verified':True,'visual_previews_verified':True,'weight_filename':'test.safetensors','size_mb':120})
        self.assertEqual(r['status'],'REJECT_UNVERIFIED')
    def test_verified_only_reaches_consent(self):
        r=lora_assess({'supports_external_lora':True,'base_model_family':'SDXL','base_model_id':'A'},
           {'base_model_family':'SDXL','base_model_id':'A','revision':'rev','license':'verified-license','license_verified':True,'license_evidence_url':'https://example.org/model-license','output_use_allowed':True,'source_verified':True,'visual_previews_verified':True,'weight_filename':'test.safetensors','size_mb':120})
        self.assertEqual(r['status'],'REQUEST_USER_APPROVAL');self.assertFalse(r['can_download_now'])
    def test_commercial_scope_gated(self):
        r=lora_assess({'supports_external_lora':True,'base_model_family':'SDXL','base_model_id':'A'},
           {'base_model_family':'SDXL','base_model_id':'A','revision':'rev','license':'verified-license','license_verified':True,'license_evidence_url':'https://example.org/model-license','output_use_allowed':True,'source_verified':True,'visual_previews_verified':True,'weight_filename':'test.safetensors','size_mb':120},True)
        self.assertEqual(r['status'],'REJECT_UNVERIFIED')
if __name__=='__main__': unittest.main()
