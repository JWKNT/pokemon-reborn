"""Read the current owned battler's normal Q popup and public field label.

Uses only Q from a verified command, then bounded Up focus within that same
owned popup. Never presses W or reads battle logs/runtime state.
"""
import argparse,json,re,time
from pathlib import Path
from play import act,snap

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('actor');p.add_argument('output',type=Path);p.add_argument('--fresh-turn',action='store_true',help='Required: native Q resets all queued choices, so inspect only before any turn action is selected.');a=p.parse_args();assert a.fresh_turn, 'Native Q resets queued doubles choices; require --fresh-turn before any turn action'
assert not a.output.exists()
norm=lambda s:re.sub('[^a-z]','',s.lower()).replace('suampert','swampert').replace('sylueon','sylveon').replace('sylweon','sylveon').replace('sulueon','sylveon').replace('sulveon','sylveon')
def capture():
 rows=snap();return '\n'.join(r['text'] for r in rows)
t=capture();assert 'fight' in t.lower() and 'bag' in t.lower(),t
assert norm(a.actor) in norm(t),t
act('q:.12','wait:.5')
observations=[]
for i in range(5):
 t=capture()
 assert 'inspecting'+norm(a.actor) in norm(t),('Owned popup required',t)
 observations.append({'epoch':time.time(),'text':t})
 if 'fieldeffect' in norm(t):break
 assert i<4,('Public field label not visible; no further input',t)
 act('up:.12','wait:.25')
a.output.write_text(json.dumps({'actor':a.actor,'observations':observations,'source':'normal owned Q inspection; no battle action'},indent=2)+'\n')
act('x','wait:.5');t=capture();assert 'fight' in t.lower() and 'bag' in t.lower(),t
print(json.dumps(observations,indent=2))
