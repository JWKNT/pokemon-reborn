"""Swap the lead from the frozen Bag, then immediately return to Bag."""
from play import *
from chest_safe_pause import classify
from party_cursor import selected_card,selection_path
import difflib
name=sys.argv[1].lower()
if '--party-open' not in sys.argv:
 assert classify(snap())=='bag'
 act('x:.12','wait:1','up:.12','c:.12','wait:1.2')
r=snap();assert classify(r)=='party'
hits=[]
for v in r:
 if .1<v['y']<.7 and difflib.SequenceMatcher(None,name,re.sub('[^a-z]','',v['text'].lower())).ratio()>=.78:
  col=int(v['x']>.5);row=round((v['y']-(.15 if not col else .195))/.21);hits.append(row*2+col)
assert len(hits)==1 and 0<=hits[0]<6
slot=hits[0]
if slot:
 act(*selection_path(selected_card(STATE),slot),'a:.12','wait:.4',*selection_path(slot,0),'c:.12','wait:.7')
 r=snap();assert any(v['x']<.5 and .1<v['y']<.3 and difflib.SequenceMatcher(None,name,re.sub('[^a-z]','',v['text'].lower())).ratio()>=.78 for v in r)
act('x:.12','wait:1','down:.12','c:.12','wait:1.2');assert classify(snap())=='bag'
c=json.loads((ROOT/'notes/current-run-control.json').read_text());p=ROOT/c['active_gauntlet_journal'];j=json.loads(p.read_text());j.setdefault('party_order_changes',[]).append({'epoch':time.time(),'swapped_slots':[slot,0],'new_lead':name,'basis':'Public party name/position verified'});p.write_text(json.dumps(j,indent=2))
print('LEAD VERIFIED; BAG PAUSED',name,flush=True)
