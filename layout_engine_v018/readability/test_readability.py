import sys
import copy
import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from audit_and_repair import run

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tests'))
from font_fixtures import local_font
F, _, FAMILY = local_font('latin')

class ReadabilityRegression(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.d=Path(self.t.name)
        self.base={
            'canvas':{'width':480,'height':660,'background':'#ffffff','safe_margin':16},
            'h0':{'id':'h0','mode':'STANDARD_BLOCK','text':'EVENT','lines':['EVENT'],
                  'x':40,'y':60,'max_width':370,'font_file':F,'font_family':FAMILY,
                  'font_size':64,'fill':'#ffffff','lock_position':True},
            'text_blocks':[],'readability_policy':{'thumbnail_scale':0.25,'max_repair_rounds':2}
        }
    def scene(self,pix):
        path=self.d/'scene.png'
        Image.fromarray(pix,'RGB').save(path)
        return str(path)
    def verify(self,plan,basename):
        path=self.d/(basename+'.json');path.write_text(json.dumps(plan))
        return run(path,self.d/basename)
    def make_scene(self,rgb):
        a=np.zeros((660,480,3),np.uint8);a[:,:,:]=rgb;return a
    def test_light_text_on_light_image_auto_recolor(self):
        p=copy.deepcopy(self.base)
        p['hero']={'file':self.scene(self.make_scene((248,248,248))),'x':0,'y':0,'width':480,'height':660}
        p['h0']['approved_text_colors']=['#1a1a1a']
        r=self.verify(p,'light')
        self.assertEqual(r['technical_readability_gate'],'PASS')
        self.assertTrue(any(c['type']=='approved_color' for c in r['change_log']))
    def test_dark_text_on_dark_image_auto_recolor(self):
        p=copy.deepcopy(self.base)
        p['hero']={'file':self.scene(self.make_scene((12,15,24))),'x':0,'y':0,'width':480,'height':660}
        p['h0']['fill']='#161b26';p['h0']['approved_text_colors']=['#ffffff']
        r=self.verify(p,'dark')
        self.assertEqual(r['technical_readability_gate'],'PASS')
    def test_busy_background_needs_relocation(self):
        p=copy.deepcopy(self.base)
        rng=np.random.default_rng(45)
        a=self.make_scene((248,248,248))
        a[92:126,:,:]=rng.choice([10,250],size=(34,480,1))
        p['hero']={'file':self.scene(a),'x':0,'y':0,'width':480,'height':660}
        p['h0']['fill']='#101010';p['h0']['y']=60;p['h0']['lock_position']=False
        p['readability_policy']['max_relocation_fraction']=0.085
        r=self.verify(p,'busy')
        self.assertEqual(r['technical_readability_gate'],'PASS',r['findings'])
        self.assertTrue(any(c['type']=='relocate' for c in r['change_log']))
    def test_local_uneven_luminance_fails_not_whole_average(self):
        p=copy.deepcopy(self.base)
        a=self.make_scene((255,255,255));a[:,165:,:]=(22,22,22)
        p['hero']={'file':self.scene(a),'x':0,'y':0,'width':480,'height':660}
        p['h0']['fill']='#161616';p['h0']['lock_position']=True
        r=self.verify(p,'uneven')
        self.assertEqual(r['technical_readability_gate'],'FAIL')
        self.assertIn('LOCAL_CONTRAST_FAIL',r['findings'][0]['reasons'])
        self.assertTrue(r['must_escalate_layout'])
    def test_protected_subject_collision_does_not_auto_hide_subject(self):
        p=copy.deepcopy(self.base)
        p['hero']={'file':self.scene(self.make_scene((10,10,10))),'x':0,'y':0,'width':480,'height':660}
        p['protected_regions']=[{'id':'person-face','x':40,'y':76,'width':200,'height':90,'importance':'critical'}]
        p['h0']['lock_position']=True
        r=self.verify(p,'subject')
        self.assertEqual(r['technical_readability_gate'],'FAIL')
        self.assertIn('IMPORTANT_SUBJECT_OVERLAP',r['findings'][0]['reasons'])
    def test_small_h0_not_claimed_visible_on_thumb(self):
        p=copy.deepcopy(self.base)
        p['hero']={'file':self.scene(self.make_scene((0,0,0))),'x':0,'y':0,'width':480,'height':660}
        p['h0']['font_size']=27
        r=self.verify(p,'tiny')
        self.assertEqual(r['technical_readability_gate'],'FAIL')
        self.assertIn('KEY_TEXT_TOO_SMALL_AT_THUMBNAIL',r['findings'][0]['reasons'])
    def test_unapproved_tint_cannot_be_silently_injected(self):
        p=copy.deepcopy(self.base)
        p['hero']={'file':self.scene(self.make_scene((240,240,240))),'x':0,'y':0,'width':480,'height':660}
        p['local_readability_treatments']=[{'x':20,'y':50,'width':250,'height':90,'fill':'#000000','opacity':0.5}]
        with self.assertRaisesRegex(Exception,'NOT_AUTHORIZED'):
            self.verify(p,'unsafe_tint')

if __name__=='__main__':unittest.main()

# Extra tests are loaded through unittest discover below in a separate class.
class ApprovalRegression(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.d=Path(self.t.name)
    def test_render_bound_visual_review_allows_final(self):
        from audit_and_repair import run
        plan={'canvas':{'width':480,'height':660,'background':'#080808','safe_margin':20},
          'h0':{'id':'h0','text':'EVENT','x':40,'y':60,'max_width':380,'font_file':F,'font_family':FAMILY,'font_size':62,'fill':'#ffffff'},'text_blocks':[]}
        path=self.d/'base.json';path.write_text(json.dumps(plan))
        output=self.d/'approved'
        one=run(path,output)
        self.assertEqual(one['technical_readability_gate'],'PASS')
        self.assertFalse(one['final_delivery_allowed'])
        review={'render_sha256':one['render_sha256'],'decision':'PASS','reviewer':'design-agent-with-image-inspection',
            'observations':{k:'Reviewed actual render and checked contrast, shape and image relationship.'
             for k in ('text_over_subject','font_personality','type_hierarchy','thumbnail_readability','hero_visual_integrity')}}
        fp=self.d/'review.json';fp.write_text(json.dumps(review))
        two=run(path,output,visual_review_file=fp)
        self.assertTrue(two['final_delivery_allowed'])
        review['render_sha256']='badprevioussha'
        fp.write_text(json.dumps(review))
        three=run(path,output,visual_review_file=fp)
        self.assertFalse(three['final_delivery_allowed'])
        self.assertEqual(three['visual_review_status'],'REJECTED_INVALID_OR_STALE')

class NoScoreGaming(unittest.TestCase):
    def test_lowering_threshold_rejected(self):
        from audit_and_repair import policy_for
        with self.assertRaisesRegex(ValueError,'POLICY_WEAKENING_FORBIDDEN'):
            policy_for({'readability_policy':{'contrast_body':2.0}})
    def test_larger_thumbnail_factor_rejected(self):
        from audit_and_repair import policy_for
        with self.assertRaisesRegex(ValueError,'POLICY_WEAKENING_FORBIDDEN'):
            policy_for({'readability_policy':{'thumbnail_scale':0.8}})
