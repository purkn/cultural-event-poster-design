import sys,unittest,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from font_coverage import assess
from render_type_specimen import make_proof

class TypeAssuranceTests(unittest.TestCase):
    def test_missing_font_errors(self):
        with self.assertRaises(FileNotFoundError):assess('/nonexistent/lorem.otf','壁上万象')
    def test_actual_font_cjk_and_proof(self):
        candidate=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
        if not candidate.exists():self.skipTest('No local Noto CJK font in environment')
        r=assess(str(candidate),'壁上万象',face_index=2,locale='zh-CN')
        self.assertTrue(r['coverage_ok']);self.assertEqual(r['glyphs_checked'],4)
        self.assertTrue(r['sha256']);self.assertEqual(r['browser_font_loaded'],'NOT_VERIFIED')
        with tempfile.TemporaryDirectory() as tmp:
            proof=Path(tmp)/'specimen.png'
            s=make_proof(str(candidate),'壁上万象',str(proof),face_index=2)
            self.assertTrue(proof.exists());self.assertGreater(proof.stat().st_size,2000)
            self.assertEqual(s['title'],'壁上万象')
    def test_cjk_wrong_region_face_fails(self):
        candidate=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
        if not candidate.exists():self.skipTest('No local Noto CJK font')
        r=assess(str(candidate),'壁上万象',face_index=0,locale='zh-CN')
        self.assertFalse(r['coverage_ok'])
        self.assertEqual(r['regional_face_match'],False)
    def test_missing_glyph_is_flagged(self):
        candidate=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
        if not candidate.exists():self.skipTest('No DejaVu font in environment')
        r=assess(str(candidate),'壁上万象',face_index=0,locale='zh-CN')
        self.assertFalse(r['coverage_ok']);self.assertGreater(len(r['missing']),0)
if __name__=='__main__':unittest.main()
