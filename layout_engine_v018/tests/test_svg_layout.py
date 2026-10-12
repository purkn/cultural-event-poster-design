import tempfile, sys, json, unittest
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_poster_svg import generate, LayoutError

CANDIDATES=[
'/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf',
'/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
'/System/Library/Fonts/PingFang.ttc'
]
F=next((p for p in CANDIDATES if Path(p).is_file()),None)

@unittest.skipUnless(F,'Test requires local CJK font; set in test fixture')
class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'out.svg'
        self.plan={
          'canvas':{'width':1080,'height':1350,'background':'#F7F7F3','safe_margin':48},
          'h0':{'mode':'STANDARD_BLOCK','id':'h0','text':'美味发酵节','lines':['美味发酵节'],'x':66,'y':92,'max_width':960,'font_file':F,'face_index':0,'font_family':'Noto Sans CJK SC','font_size':120,'fill':'#151515'},
          'text_blocks':[{'id':'date','text':'2026.10.14 - 10.18','x':70,'y':1090,'max_width':900,'font_file':F,'font_family':'Noto Sans CJK SC','font_size':36,'fill':'#151515'}]
        }
    def test_svg_contains_editable_text(self):
        generate(self.plan,self.path)
        root=ET.parse(self.path).getroot()
        txt=root.findall('{http://www.w3.org/2000/svg}text')
        self.assertEqual(len(txt),2)
        self.assertEqual(''.join(txt[0].itertext()),'美味发酵节')
        self.assertNotIn('transform',txt[0].attrib)
    def test_wrong_character_lines_blocked(self):
        self.plan['h0']['lines']=['美味发酵日']
        with self.assertRaisesRegex(LayoutError,'SOURCE_LINES_MISMATCH'):generate(self.plan,self.path)
    def test_unsupported_per_character_blocked(self):
        self.plan['h0']['char_sizes']=[120,135,113,180,101]
        with self.assertRaisesRegex(LayoutError,'PER_GLYPH_VARIATION_FORBIDDEN'):generate(self.plan,self.path)
    def test_unknown_font_is_blocked(self):
        self.plan['h0']['font_file']='/tmp/no-this-font-ever.otf'
        with self.assertRaisesRegex(LayoutError,'FONT_FILE_MISSING'):generate(self.plan,self.path)
    def test_region_overflow_blocked(self):
        self.plan['h0']['max_width']=100
        with self.assertRaisesRegex(LayoutError,'H0_HORIZONTAL_OVERFLOW'):generate(self.plan,self.path)
    def test_safe_area_blocked(self):
        self.plan['h0']['x']=0
        with self.assertRaisesRegex(LayoutError,'H0_REGION_OUTSIDE_SAFE_AREA'):generate(self.plan,self.path)
    def test_text_collision_blocked(self):
        self.plan['text_blocks'][0]['x']=70
        self.plan['text_blocks'][0]['y']=100
        with self.assertRaisesRegex(LayoutError,'TEXT_BLOCK_COLLISION'):generate(self.plan,self.path)
    def test_custom_glyph_requires_proof(self):
        self.plan['h0']['mode']='CUSTOM_GLYPH'
        with self.assertRaisesRegex(LayoutError,'CUSTOM_GLYPH_NEEDS_REFERENCE'):generate(self.plan,self.path)
    def test_no_visual_pass_claim(self):
        generate(self.plan,self.path)
        self.assertTrue(self.path.is_file())
    def test_h0_wrong_fill(self):
        self.plan['h0']['fill']='cyan'
        with self.assertRaisesRegex(LayoutError,'INVALID_COLOR'):generate(self.plan,self.path)
    def test_h0_explicit_line_break_consistency(self):
        self.plan['h0']['lines']=['美味','发酵节']
        self.plan['h0']['line_spacing']=130
        generate(self.plan,self.path)
        self.assertEqual(len(ET.parse(self.path).getroot().findall('.//{http://www.w3.org/2000/svg}tspan')),3)

if __name__=='__main__':unittest.main()
