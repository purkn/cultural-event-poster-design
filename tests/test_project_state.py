import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from workflow_state import fresh,decide,guard,invalidate
class StateTests(unittest.TestCase):
 def ready(self):
  s=fresh();decide(s,'input','资料确认');decide(s,'style','选剪纸','S1');return s
 def test_no_skip(self):
  with self.assertRaises(ValueError):guard(fresh(),'hero_a')
  with self.assertRaises(ValueError):decide(fresh(),'visual','B','B')
 def test_title_blocked_until_choice(self):
  s=self.ready();self.assertTrue(guard(s,'hero_a'))
  with self.assertRaises(ValueError):guard(s,'h0')
  decide(s,'visual','选B','B');self.assertTrue(guard(s,'h0'))
 def test_reopen_invalidates_downstream(self):
  s=self.ready();decide(s,'visual','A','A');invalidate(s,'style','换风格')
  self.assertEqual(s['checkpoints']['input']['status'],'confirmed')
  with self.assertRaises(ValueError):guard(s,'hero_a')
 def test_feedback_after_delivery(self):
  s=self.ready();decide(s,'visual','A','A')
  with self.assertRaises(ValueError):decide(s,'feedback','满意')
  s['stage']='feedback_review';decide(s,'feedback','字体普通');self.assertEqual(s['stage'],'improvement_review')
  with self.assertRaises(ValueError):guard(s,'h0')
 def test_cannot_overwrite_choice(self):
  s=self.ready()
  with self.assertRaises(ValueError):decide(s,'style','换成S8','S8')
 def test_silence_not_approval(self):
  with self.assertRaises(ValueError):decide(fresh(),'input',' ')
if __name__=='__main__':unittest.main()
