"""Bounded encounter search in a reviewed safe walking corridor; UI only."""
from play import *
import argparse,re
p=argparse.ArgumentParser();p.add_argument('--targets',default='skorupi,drapion');p.add_argument('--cycles',type=int,default=90);p.add_argument('--vertical',action='store_true');a=p.parse_args();walk=0
for _ in range(a.cycles):
 r=snap();t=' '.join(v['text'] for v in r);lo=t.lower();print(t,flush=True)
 if any(n in lo for n in a.targets.split(',')):print('TARGET FOUND',flush=True);break
 if 'fight' in lo:
  if subprocess.call([sys.executable,str(ROOT/'scripts/flee.py')]):raise SystemExit('Escape needs review')
  continue
 if 'pp:' in lo or re.search(r'pp.?\s*\d+[/0]\d+',lo):act('x','wait:0.4');continue
 if 'fainted' in lo:raise SystemExit('Faint review')
 if any(w in lo for w in ['hp','wild ','appeared']):act('wait:1');continue
 if 'repel' in lo and 'wore off' in lo:
  act('c','wait:0.4');z=read().lower()
  if 'another' in z:act('x','wait:0.4')
  continue
 if len(r)>4 or any(w in lo for w in ['yes','no','choose','menu']):raise SystemExit('Unexpected screen')
 seq=[]
 for j in range(4):
  direction=('up' if walk%2==0 else 'down') if a.vertical else ('left' if walk%2==0 else 'right')
  seq.append(direction+':0.62');walk+=1
 act(*seq,'wait:0.2')
else:print('Search limit reached',flush=True)
