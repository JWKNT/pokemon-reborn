"""Swap party lead with an explicitly chosen slot; requires Pokemon remembered in main menu."""
from play import *
import re,difflib
wanted=sys.argv[1];i=int(wanted) if wanted.isdigit() else None
if i is not None:assert 0<=i<6
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'would you like to save' in t:
 act('x','wait:2','x','wait:2','x','wait:2',*(['up:0.22']*4),'c','wait:2');t=read().lower()
if 'pokedex' in t and ('seen' in t or 'search' in t):
 act('x','wait:1.5','down','c','wait:1.6');t=read().lower()
if sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3 or ('sort' in t and any(k in t for k in ['medicine','medieine','items','berries'])) or 'sort a:' in t or ('close bag' in t) or ('rock smash' in t and any(w in t for w in ['charge beam','safeguard','nature power'])):
 act('x','wait:1.5','up','c','wait:1.6');t=read().lower()
if not ('cancel' in t and t.count('hp')>=5):raise SystemExit('Party entry review: '+t)
# Resolve a named lead from the observed grid, without relying on prior order.
if i is None:
 candidates=[]
 for v in snap():
  score=difflib.SequenceMatcher(None,wanted.lower(),re.sub('[^a-z]','',v['text'].lower())).ratio()
  if score>=.78 and .1<v['y']<.7:
   col=int(v['x']>.5);row=round((v['y']-(.15 if not col else .195))/.21)
   if row in [0,1,2]:candidates.append((score,row*2+col))
 if not candidates:raise SystemExit('Named lead was not found')
 i=max(candidates)[1]
if i==0:
 subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True);raise SystemExit(0)
# A new party menu starts at index0; this helper only opens fresh from overworld.
act('a',*(['down:0.05']*(i//2)),*(['right:0.05'] if i%2 else []),'c','wait:2')
print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
