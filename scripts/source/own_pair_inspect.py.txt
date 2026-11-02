"""Inspect the two OWN allies before any double turn selection; never W.
Q maps to installed L, whose chooseInspectSlot(0,current) only cycles even slots.
Opening Q after registering a choice would cancel it, so callers use this only
at the first actor's fresh command, before either choice is registered.
"""
import argparse,json,re,time,difflib
from pathlib import Path
from play import act,snap,ROOT
p=argparse.ArgumentParser();p.add_argument('first');p.add_argument('second');p.add_argument('output',type=Path);a=p.parse_args();assert not a.output.exists()
norm=lambda s:re.sub('[^a-z]','',s.lower()).replace('sylweon','sylveon').replace('sywveon','sylveon').replace('syweon','sylveon').replace('sylueon','sylveon').replace('sulueon','sylveon').replace('suampert','swampert').replace('sulveon','sylveon').replace('areanine','arcanine').replace('krickertune','kricketune').replace('nricketune','kricketune')
src=Path('/Applications/Reborn.app/Contents/Game/Scripts/Battle_Inspect.rb').read_text();assert 'battleindex = chooseInspectSlot(0, pkmn.index)'in src
rows=snap();t=' '.join(v['text']for v in rows);prompt=' '.join(v['text']for v in rows if v['y']>.72 and v['x']<.55)
assert 'fight'in t.lower()and'bag'in t.lower()and norm(a.first)in norm(prompt),(t,prompt)
proof=[]
for name in [a.first,a.second]:
 act('q:.12','wait:.4');obs=[]
 for i in range(5):
  rows=snap();t='\n'.join(v['text']for v in rows);assert 'inspecting' in norm(t) and difflib.SequenceMatcher(None,norm(t).split('inspecting')[-1],norm(name)).ratio()>=.82,('Owned ally popup required',t)
  obs.append(dict(epoch=time.time(),text=t))
  if 'fieldeffect'in norm(t):break
  assert i<4;act('up:.12','wait:.25')
 proof.append(dict(actor=name,observations=obs))
a.output.write_text(json.dumps(dict(source='Normal Q only; both own allies before turn registration',allies=proof),indent=2)+'\n')
act('x','wait:.4');t=' '.join(v['text']for v in snap());assert 'fight'in t.lower()and'bag'in t.lower(),t
print(json.dumps(proof,indent=2))
