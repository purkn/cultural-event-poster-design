import sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
from preflight_brief import assess as brief_assess

def field(value):return {'value':value,'status':'confirmed' if value else 'missing','source':'user_text' if value else None}
class GateTests(unittest.TestCase):
    def test_missing_date_location_stops(self):
        r=brief_assess({'poster_purpose':'announcement','event_mode':'offline','fields':{'title_zh':field('文化节')}})
        self.assertEqual(r['status'],'WAITING_FOR_USER');self.assertFalse(r['may_generate_hero']);self.assertEqual(len(r['blocking_missing']),2)
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
if __name__=='__main__': unittest.main()
