"""Behavioral regression of recommendation constraints and actual layer delivery."""
import copy,importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from recommend_design import recommend
from compose_layers import compose
from validate_output import validate

def profile():
    p={'activity_id':'synthetic-workshop','activity_type':'workshop','theme_tags':['nature','craft'],'audience':['families'],'mood':{'primary':'warm','secondary':[]},'communication':{'channel':'print','density':'medium'},'evidence':{}}
    for k in ['theme_tags.nature','theme_tags.craft','audience.families','mood.warm','communication.print']:p['evidence'][k]={'source':'synthetic test brief','confidence':1}
    return p
class Matching(unittest.TestCase):
    def test_theme_mood_are_hints_not_old_bucket(self):self.assertEqual(recommend(profile())['candidates'][0]['style'],'S1')
    def test_explicit_choice_wins(self):
        p=profile();p['constraints']={'allowed_style_ids':['S6']};r=recommend(p);self.assertTrue(r['candidates']);self.assertTrue(all(x['style']=='S6' for x in r['candidates']));self.assertFalse(r['checkpoint_approved'])
    def test_reference_is_constraint(self):
        p=profile();p['reference_constraint']=True;p['reference_assessments']={'S8':{'compatible':True,'evidence':['synthetic manual review'],'score':0.8}}
        rows=recommend(p)['candidates'];self.assertTrue(rows);self.assertTrue(all(x['style']=='S8' for x in rows))
    def test_no_reference_evidence_no_fallback(self):
        p=profile();p['reference_constraint']=True;self.assertEqual(recommend(p)['candidates'],[])
    def test_experimental_style_can_hold_dense_network(self):
        p=profile();p['communication']['density']='high';p['constraints']={'allowed_style_ids':['S6'],'allowed_layout_ids':['M06']};self.assertTrue(recommend(p)['candidates'])
    def test_no_arbitrary_style_layout_whitelist(self):
        p=profile();p['constraints']={'allowed_style_ids':['S3'],'allowed_layout_ids':['M05']};r=recommend(p);self.assertTrue(r['candidates']);self.assertEqual(r['candidates'][0]['topology_preference_bonus'],0)
    def test_capacity_requires_case_evidence(self):
        p=profile();p['communication']['density']='high';p['constraints']={'allowed_style_ids':['S6'],'allowed_layout_ids':['M01']};self.assertEqual(recommend(p)['candidates'],[])
        p['layout_assessments']={'M01':{'capacity_ok':True,'evidence':'synthetic trial layout fits'}};self.assertTrue(recommend(p)['candidates'])
    def test_capacity_failure_overrides_natural_density(self):
        p=profile();p['constraints']={'allowed_layout_ids':['M01']};p['layout_assessments']={'M01':{'capacity_ok':False,'evidence':'real title cannot fit'}};self.assertEqual(recommend(p)['candidates'],[])
    def test_medium_direction_not_new_taxonomy(self):
        p=profile();a=recommend(p)['candidates'];p['parameters']={'medium':'photography','direction':'diagonal'};b=recommend(p)['candidates'];self.assertEqual([(x['style'],x['layout']) for x in a],[(x['style'],x['layout']) for x in b]);self.assertEqual(b[0]['parameters'],p['parameters'])
    def test_no_silent_old_F_id_mapping(self):
        p=profile();p['constraints']={'allowed_style_ids':['F04']};self.assertEqual(recommend(p)['status'],'needs_taxonomy_migration')
    def test_reality_intervention_requires_scene(self):
        p=profile();p['constraints']={'allowed_style_ids':['S2']};r=recommend(p);self.assertEqual(r['candidates'],[]);self.assertTrue(any('实景' in x['reason'] for x in r['rejected']))
    def test_reliable_existing_scene_enables_S2(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'scene.png';Image.new('RGB',(16,16)).save(f)
            p=profile();p['constraints']={'allowed_style_ids':['S2']};p['materials']={'scene_photo':{'verified':True,'source':'synthetic test image reviewed','path':str(f)}};self.assertTrue(recommend(p)['candidates'])
    def test_no_silent_old_id_mapping(self):
        p=profile();p['constraints']={'allowed_style_ids':['P07']};r=recommend(p);self.assertEqual(r['status'],'needs_taxonomy_migration');self.assertEqual(r['candidates'],[])
    def test_old_layout_constraint_also_needs_migration(self):
        p=profile();p['constraints']={'excluded_layout_ids':['L01']};self.assertEqual(recommend(p)['status'],'needs_taxonomy_migration')
    def test_repeat_penalty_preserves_user_choice(self):
        p=profile();p['constraints']={'allowed_style_ids':['S1']};p['history']=[{'style':'S1','layout':'M01'}]*3;r=recommend(p);self.assertNotEqual(r['candidates'][0]['layout'],'M01');self.assertTrue(all(x['style']=='S1' for x in r['candidates']))
    def test_old_history_not_miscounted(self):
        p=profile();p['history']=[{'style':'P07','layout':'L01'}]*10;r=recommend(p);self.assertTrue(all(x['repeat_penalty']==0 for x in r['candidates']));self.assertTrue(any('历史' in x for x in r['warnings']))
    def test_low_confidence_stays_explained(self):
        p=profile();p['evidence']['mood.warm']['confidence']=0.2;r=recommend(p);self.assertTrue(any('mood.warm' in x for x in r['warnings']));self.assertFalse(r['checkpoint_approved'])
    def test_invalid_confidence_rejected(self):
        p=profile();p['evidence']['mood.warm']['confidence']=float('nan')
        with self.assertRaises(ValueError):recommend(p)
    def test_no_evidence_no_default_template(self):
        p=profile();p['evidence']={};r=recommend(p);self.assertEqual(r['status'],'needs_design_evidence');self.assertEqual(r['candidates'],[])
    def test_channel_not_guessed_from_family(self):
        p=profile();r=recommend(p);self.assertTrue(all(x['components']['C']==0 for x in r['candidates']));self.assertTrue(any('渠道' in x for x in r['warnings']))
class Delivery(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.project=self.root/'project'
        Image.new('RGB',(160,200),'black').save(self.root/'hero.png')
        for name,box in [('title',(15,10,120,65)),('text',(15,120,120,165))]:
            im=Image.new('RGBA',(160,200));ImageDraw.Draw(im).rectangle(box,fill='white');im.save(self.root/(name+'.png'))
    def tearDown(self):self.temp.cleanup()
    def produce(self):return compose(self.root/'hero.png',self.root/'title.png',self.root/'text.png',self.project,'zh')
    def add_records(self):
        md=self.project/'06_metadata'
        (self.project/'05_source/text_zh.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="200"><text x="15" y="140">Synthetic test body</text></svg>')
        fields={k:{'value':'synthetic','status':'provided','source':'test fixture'} for k in ['theme','purpose','dates','venue_or_online','organizer','description','audience','registration']}
        fields['languages']={'value':['zh'],'status':'provided','source':'test fixture'};fields['output_dimensions']={'value':[160,200],'status':'provided','source':'test fixture'}
        (md/'activity.json').write_text(json.dumps({'fields':fields}))
        quality={'hard_gates':{k:{'status':'PASS','evidence':'synthetic test only'} for k in ['text_accuracy','readability','layer_integrity','content_completeness']},'aesthetics':{k:{'score':4,'evidence':'synthetic test only'} for k in ['design_quality','style_consistency']},'design_review':{'verdict':'PASS','evidence':'synthetic test only'}}
        (md/'quality_zh.json').write_text(json.dumps(quality))
        (md/'workflow_state.json').write_text(json.dumps({'schema_version':1,'pending_checkpoint':None,'checkpoints':{k:{'status':'confirmed','quote':'synthetic approval, test only','selection':k} for k in ['input','style','visual']}}))
        blocks=[{'id':'t','bbox':[10,5,120,70],'color':'#FFFFFF','font_px':60,'role':'h0'},{'id':'b','bbox':[10,115,120,60],'color':'#FFFFFF','font_px':32,'role':'body'}]
        (self.root/'blocks.json').write_text(json.dumps(blocks))
        subprocess.run([sys.executable,str(ROOT/'scripts/check_text_readability.py'),'--final',str(self.project/'01_final/poster_zh.png'),'--background',str(self.project/'02_hero/hero_zh.png'),'--text-layer',str(md/'text_combined_zh.png'),'--blocks',str(self.root/'blocks.json'),'--out',str(md/'readability_zh.json')],check=True,stdout=subprocess.DEVNULL)
    def test_real_compose_and_validate(self):self.produce();self.add_records();self.assertEqual(validate(self.project,'zh'),[])
    def test_no_fake_formal_delivery(self):self.produce();self.assertTrue(validate(self.project,'zh'))
    def test_no_silent_resize(self):
        Image.new('RGBA',(16,20)).save(self.root/'title.png')
        with self.assertRaises(ValueError):self.produce()
    def test_no_opaque_title(self):
        Image.new('RGBA',(160,200),'white').save(self.root/'title.png')
        with self.assertRaises(ValueError):self.produce()
    def test_no_empty_title(self):
        Image.new('RGBA',(160,200)).save(self.root/'title.png')
        with self.assertRaises(ValueError):self.produce()
    def test_no_overwrite(self):
        self.produce()
        with self.assertRaises(FileExistsError):self.produce()
    def test_raster_body_cannot_claim_editable_text(self):
        self.produce();self.add_records();(self.project/'05_source/text_zh.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="body.png"/></svg>');self.assertTrue(any('editable text' in x for x in validate(self.project,'zh')))
    def test_pending_checkpoint_blocks_delivery(self):
        self.produce();self.add_records();p=self.project/'06_metadata/workflow_state.json';v=json.loads(p.read_text());v['pending_checkpoint']='B';p.write_text(json.dumps(v));self.assertTrue(any('checkpoint' in x for x in validate(self.project,'zh')))
    def test_modified_output_rejected(self):
        self.produce();self.add_records();Image.new('RGB',(160,200),'red').save(self.project/'01_final/poster_zh.png');self.assertTrue(any('composition' in x for x in validate(self.project,'zh')))
    def test_stale_report_rejected(self):
        self.produce();self.add_records();p=self.project/'06_metadata/readability_zh.json';v=json.loads(p.read_text());v['inputs']['final_sha256']='old';p.write_text(json.dumps(v));self.assertTrue(any('stale' in x for x in validate(self.project,'zh')))
    def test_unresolved_p1_blocks_formal_delivery(self):
        self.produce();self.add_records();p=self.project/'06_metadata/activity.json';v=json.loads(p.read_text());v['fields']['dates']['status']='pending';p.write_text(json.dumps(v));self.assertTrue(any('dates' in x for x in validate(self.project,'zh')))
if __name__=='__main__':unittest.main()
