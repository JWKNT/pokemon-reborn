"""Shake one inspected Route4 tree; stop at the public wild battle prompt."""
from play import *
from locate import locate
assert locate(710)==(710,28,40)
act('up:.18','c','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
for _ in range(30):
 t=read();print(t,flush=True);low=t.lower()
 if 'fight' in low or ('what will' in low and 'run' in low):break
 if any(z in low for z in ['nope.','nothing']):
  act('c','wait:.5');print('EMPTY TREE',flush=True);break
 if 'used headbutt' in low:act('c','wait:.5');continue
 if 'wild' in low or 'hp' in low:act('wait:.6');continue
 if len(re.sub('[^a-z]','',low).replace('pokemonreborn',''))<3:act('wait:.7');continue
 raise SystemExit('Headbutt result review: '+t)
else:raise SystemExit('No battle ready; inspect whether tree empty')
