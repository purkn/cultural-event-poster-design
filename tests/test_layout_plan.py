import sys,unittest,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_layout_plan import check
class LayoutTests(unittest.TestCase):
 def plan(self):return {'topology':'M01','spatial_mode':'V06','canvas':[1080,1350],'orientation':'portrait','title_skeleton':{'text':'一起编织吧','lines':['一起','编织吧']},'selection_reason':'单物件中心焦点','rejected_alternative':'V01窄带无法容纳长事实','capacity_evidence':'标题粗排和实际行数待看图复核','reading_path':'标题到主体到事实','regions':[{'role':'title','x':5,'y':5,'w':80,'h':15,'z_order':1,'allow_overlap':False}],'protected_regions':[]}
 def test_catalog(self):
  modes=json.loads((ROOT/'libraries/layouts/spatial_modes.json').read_text())['modes'];self.assertEqual(len(modes),18);self.assertEqual(len({m['id'] for m in modes}),18)
 def test_orientation(self):
  p=self.plan();self.assertEqual(check(p)['status'],'GEOMETRY_OK');p['spatial_mode']='H01';self.assertTrue(check(p)['errors'])
 def test_outside(self):
  p=self.plan();p['regions'][0]['w']=100;self.assertTrue(check(p)['errors'])
 def test_exact_title(self):
  p=self.plan();p['title_skeleton']['lines']=['一起','编织'];self.assertTrue(check(p)['errors'])
 def test_protected_is_review(self):
  p=self.plan();p['protected_regions']=[{'role':'face','x':6,'y':6,'w':10,'h':10}];r=check(p);self.assertEqual(r['status'],'REVIEW');self.assertFalse(r['errors'])
 def test_square_not_silent(self):
  p=self.plan();p['canvas']=[1080,1080];p['orientation']='square';self.assertTrue(check(p)['errors'])
if __name__=='__main__':unittest.main()
