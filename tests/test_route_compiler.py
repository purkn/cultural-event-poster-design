import unittest, importlib.util, copy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('routes',ROOT/'scripts'/'compile_routes.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def fresh_route(id,lead_id,palette,type_family,concept_id):
    if lead_id=='P09':
        img='reference_library/collections/keyword-20261012/images/REF-001_文化节庆_自由拼贴_手写_蓝黄.jpg'
        med='large simplified outline and loose pastel-flat color accents'
        structure='one dominant image mass under loose black heading'
        dna='brushy informal lettering with a black strong headline'
        val='high_key'
    else:
        img='reference_library/collections/keyword-20261012/images/REF-002_文化节庆_模块化网格_无衬线_绿米白.jpg'
        med='black delicate freehand ink drawing with restrained spot colors'
        structure='type concentrated top, narrative drawings in open center, compact small information below'
        dna='high contrast clean narrow black Chinese typography, editorially arranged'
        val='high_key'
    return {
        'id':id,
        'lead':{'id':lead_id,'path':img,'observed':True,'observation_note':'实际观察：' + med+'; '+structure,'palette_family':palette,'value_regime':val,'medium':med,'type_dna':dna,'structure':structure,'classification':'STRONG_LEAD'},
        'color':{'palette_family':palette,'background_family':'fresh_white','source':'lead','background':'fresh bright paper-white, absolutely no grunge','dominant':'ink-black' if lead_id=='P05' else 'black with restrained powder-blue','secondary':'muted pale accents only'},
        'typography':{'type_family':type_family,'strategy':'verified_custom_artword','h0_design_action':'actual Chinese glyph contours with intentionally drawn and verified line rhythms, not CSS rotation','reference_reason':'title and image meet by thickness-and-silhouette relationships'},
        'concept':{'id':concept_id,'hero_subject':'one atypically cropped fermentation-process glyph','visible_mechanism':'time stages transform a linear symbol into a food texture that alters the page negative-space boundary','theme_binding':'food fermentation changes material over several days, depicted as changing contour'},
        'composition':{'hero_zone':'right two thirds rising across midheight','h0_zone':'upper left as real glyph-safe artword','info_zone':'bottom clean zone','negative_space':'intentional crescent gap around hero shape'},
        'reference_fit_reason':'The current lead has compatible page structure for a large transformation silhouette and type with enough space.',
        'negative_constraints':['no cyan-red-yellowed paper combination','no single unbroken giant jar blob','no pasted fake Chinese text','no generic children sticker illustration']
    }

def base():
    return {'schema_version':'0.17','project_id':'fermentation_hangzhou_2026','mode':'hero_rough',
            'brief':{'confirmed':True,'title':'美味发酵节','date':'2026.10.14—10.18','venue':'杭州天目里','core_experience':'发酵中的时间与食物变化'},
            'canvas':{'width':1080,'height':1350},
            'backend':{'id':'local-imagegen','supports_reference_images':False,'supports_negative_prompt':False},
            'feedback':{'project_id':'fermentation_hangzhou_2026','rejected':True,
                'previous_route':{'lead_id':'P03','palette_family':'cyan_red_warm_cream','type_family':'ZCOOL KuaiLe','concept_id':'giant_single_jar_blob','background_family':'distressed_warm_paper'},
                'must_change':['palette_family','type_family','concept_id','background_family'],
                'disliked_appearances':['muddy beige ground','red and cyan','ugly angular Chinese H0','giant featureless jar']},
            'routes':[fresh_route('alternative_1','P09','black_blue_pink','custom_black_ink_letterforms','ferment_time_path'),
                      fresh_route('alternative_2','P05','black_white_spot','fine_black_custom_title','culture_growth_grid')]}

class RouteCompilerTests(unittest.TestCase):
    def test_positive_distinct_routes(self):
        p=m.compile_routes(base(),ROOT)
        self.assertEqual(p['compile_status'],'COMPILED_NOT_RENDERED')
        self.assertEqual(p['design_status'],'NOT_VISUALLY_REVIEWED')
        self.assertEqual(len(p['routes']),2)
    def test_reject_same_color(self):
        d=base();d['routes'][0]['color']['palette_family']='cyan_red_warm_cream';d['routes'][0]['lead']['palette_family']='cyan_red_warm_cream'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('USER_REJECTED_PATTERN_REUSED:palette_family',str(e.exception))
    def test_reject_same_font(self):
        d=base();d['routes'][0]['typography']['type_family']='ZCOOL KuaiLe'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('USER_REJECTED_PATTERN_REUSED:type_family',str(e.exception))
    def test_reject_same_hero(self):
        d=base();d['routes'][0]['concept']['id']='giant_single_jar_blob'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('USER_REJECTED_PATTERN_REUSED:concept_id',str(e.exception))
    def test_reject_same_background(self):
        d=base();d['routes'][0]['color']['background_family']='distressed_warm_paper'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('USER_REJECTED_PATTERN_REUSED:background_family',str(e.exception))
    def test_reject_no_second_route(self):
        d=base();d['routes']=d['routes'][:1]
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('AT_LEAST_TWO_DIFFERENT_ROUTES_REQUIRED',str(e.exception))
    def test_reject_identical_route(self):
        d=base();d['routes'][1]=copy.deepcopy(d['routes'][0]);d['routes'][1]['id']='alternative_other'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('ROUTES_ARE_DUPLICATES',str(e.exception))
    def test_new_ids_do_not_create_visual_difference(self):
        d=base(); d['routes'][1]=copy.deepcopy(d['routes'][0])
        d['routes'][1]['id']='new-route'; d['routes'][1]['concept']['id']='new-label'
        with self.assertRaisesRegex(m.RouteError, 'ROUTES_ARE_DUPLICATES'):
            m.compile_routes(d,ROOT)
    def test_one_visual_dimension_is_insufficient(self):
        d=base(); d['routes'][1]=copy.deepcopy(d['routes'][0])
        d['routes'][1]['id']='new-route'
        d['routes'][1]['concept']['visible_mechanism']='a different visible transformation'
        with self.assertRaisesRegex(m.RouteError, 'TWO_VISUAL_DIMENSION'):
            m.compile_routes(d,ROOT)
    def test_two_visual_dimensions_are_accepted(self):
        d=base(); d['routes'][1]=copy.deepcopy(d['routes'][0])
        d['routes'][1]['id']='new-route'
        d['routes'][1]['concept']['visible_mechanism']='a different visible transformation'
        d['routes'][1]['composition']['hero_zone']='centered vertical shape'
        self.assertEqual(m.compile_routes(d,ROOT)['compile_status'],'COMPILED_NOT_RENDERED')
    def test_reject_unknown_image(self):
        d=base();d['routes'][0]['lead']['path']='missing.jpg'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('LEAD_IMAGE_NOT_FOUND',str(e.exception))
    def test_reject_unobserved(self):
        d=base();d['routes'][0]['lead']['observed']=False
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('LEAD_NOT_VISUALLY_OBSERVED',str(e.exception))
    def test_wrong_compatibility(self):
        d=base();d['routes'][0]['color']['palette_family']='totally_different'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('LEAD_COLOR_PROVENANCE_CONFLICT',str(e.exception))
    def test_metadata_breakpoint(self):
        d=base();d['brief']['venue']=''
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('BP_CONTENT_MISSING',str(e.exception))
    def test_feedback_project_scope(self):
        d=base();d['feedback']['project_id']='other_project'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('FEEDBACK_PROJECT_MISMATCH',str(e.exception))
    def test_example_file_rejected_for_production(self):
        d=base()
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT,ROOT/'examples'/'sample.json')
        self.assertIn('PRODUCTION_INPUT_CANNOT_USE_EXAMPLE_FILE',str(e.exception))
    def test_reference_image_not_claimed_sent_when_unavailable(self):
        p=m.compile_routes(base(),ROOT)
        self.assertEqual(p['backend']['reference_conditioning'],'TEXT_ONLY_REFERENCE_FALLBACK')
        self.assertEqual(p['routes'][0]['required_image_attachments'],[])
    def test_reference_request_does_not_claim_success(self):
        d=base();d['backend']['supports_reference_images']=True
        p=m.compile_routes(d,ROOT)
        self.assertEqual(p['backend']['reference_conditioning'],'REQUESTED_NOT_VERIFIED')
        self.assertTrue(p['routes'][0]['required_image_attachments'][0]['must_send_at_runtime'])
    def test_prompt_doesnt_use_old_palette(self):
        p=m.compile_routes(base(),ROOT)
        body=' '.join(x['positive_prompt'] for x in p['routes'])
        self.assertIn('Do not inherit styling from example JSON',body)
        self.assertNotIn('clear cyan-blue as a deliberate major graphic color',body)
    def test_h0_needs_glyph_proof(self):
        d=base();d['mode']='h0_artword'
        with self.assertRaises(m.RouteError) as e:m.compile_routes(d,ROOT)
        self.assertIn('H0_REQUIRES_VERIFIED_CHARACTER_SKELETON',str(e.exception))

if __name__=='__main__':unittest.main()
