import hashlib,json,re,string,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_style_prompt import templates,expand
PACKS=json.loads((ROOT/'libraries/styles/packs.json').read_text())['packs']
EXPECTED=['色块剪纸与手工拼贴','现实照片与平面介入','几何构成与现代主义','艺术字体与编辑排版','版画与套色印刷','二维图形与局部立体','像素与模块图形','留白与材料诗意']
class Guides(unittest.TestCase):
 def test_ids_names_match_attached_taxonomy(self):self.assertEqual([(p['id'],p['name']) for p in PACKS],list(zip(['S'+str(i) for i in range(1,9)],EXPECTED)))
 def test_source_guides_preserved_with_provenance(self):
  manifest=json.loads((ROOT/'libraries/styles/source-manifest.json').read_text())
  for item in manifest['files']:
   source=(ROOT/item['local_guide']).read_bytes().split(b'\n\n---\n\n## cultural-poster-flow',1)[0]
   self.assertEqual(hashlib.sha256(source).hexdigest(),item['source_sha256'])
 def test_stage_transparency_contract(self):
  for p in PACKS:
   t=templates(p['id']);self.assertEqual(set(t),{'hero_a','hero_b','h0','repair'});self.assertIs(t['h0']['transparent_background'],True);self.assertIs(t['hero_a']['transparent_background'],False);self.assertEqual(t['repair']['transparent_background'],'preserve_input')
 def test_complete_values_produce_usable_prompt(self):
  for p in PACKS:
   for stage,spec in templates(p['id']).items():
    keys={key for _,key,_,_ in string.Formatter().parse(spec['prompt']) if key};values={k:'已核定测试值-'+k for k in keys};result=expand(p['id'],stage,values);self.assertTrue(result['prompt']);self.assertNotIn('{',result['prompt']);self.assertEqual(result['style'],p['id'])
 def test_missing_values_are_not_fabricated(self):
  with self.assertRaises(ValueError):expand('S1','hero_a',{})
 def test_old_ids_cannot_select_wrong_guide(self):
  with self.assertRaises(ValueError):templates('F01')
 def test_reference_moves_keep_hashes_and_unassigned_status(self):
  for p in PACKS:
   for ref in p['reference_pool']:
    self.assertEqual(ref['new_style_membership'],'NOT_ASSIGNED');self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
 def test_simple_root_structure(self):
  self.assertEqual({p.name for p in ROOT.iterdir() if p.name not in {".git","README.md"}},{'SKILL.md','core','libraries','scripts','tests','feedback'})
 def test_real_local_markdown_links(self):
  for p in ROOT.rglob('*.md'):
   if 'legacy' in p.parts:continue
   for target in re.findall(r'\]\(([^\s)]+)\)',p.read_text()):
    if target.startswith(('http:','https:','#')):continue
    self.assertTrue((p.parent/target.split('#')[0]).exists(),str(p)+' -> '+target)
if __name__=='__main__':unittest.main()
