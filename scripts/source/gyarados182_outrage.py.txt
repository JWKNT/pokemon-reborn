"""Teach the owned Gyarados Outrage through the normal eight-shard tutor."""
from play import *
from learning import resolve,PLANS

def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)],check=True)

s=json.loads((ROOT/'notes/Gyarados181-Outrage-ready-status.json').read_text())
g=next(p for p in s['party'] if p['species']=='GYARADOS')
assert g['level']==95 and g['ev']==[0,252,0,0,0,252]
assert s['bag']['contents'].get('PURPLESHARD',0)>=8
assert [m['move'] for m in g['moves']]==['WATERFALL','TACKLE','CRUNCH','DRAGONDANCE']
run('eventq',522,125,'talk')
run('choose_dialog','Superpower|Earth Power|Outrage|Heat Wave','Outrage')
run('choose_dialog','Yes|No','Yes')
for _ in range(8):
 t=read().lower()
 if 'choose a pok' in t or 'teach which' in t or ('cancel' in t and t.count('hp')>=5):break
 if any(x.strip() in ['yes','no'] for x in t.splitlines()):raise SystemExit('Unexpected tutor choice')
 act('c','wait:.4')
else:raise SystemExit('Tutor party prompt missing')
run('party_pick','Gyarados','--single')
PLANS['outrage']=1
for _ in range(10):
 t=read()
 if 'trying to learn' in ' '.join(t.lower().split()):
  assert 'outrage' in t.lower();assert resolve(t);break
 if any(x in t.lower() for x in ['not compatible','already knows']):raise SystemExit('Tutor rejected')
 act('c','wait:.4')
else:raise SystemExit('Learning prompt missing')
for _ in range(15):
 t=read().lower()
 if all(x in t for x in ['superpower','outrage','heat wave']):
  act('x','wait:.7');break
 if any(x.strip() in ['yes','no'] for x in t.splitlines()):raise SystemExit('Unexpected tutor post-choice')
 act('c','wait:.4')
else:raise SystemExit('Tutor exit not recognized')
run('overworld');run('checkpoint','Gyarados182-Outrage-trained')
s=json.loads((ROOT/'notes/Gyarados182-Outrage-trained-status.json').read_text())
g=next(p for p in s['party'] if p['species']=='GYARADOS')
assert [m['move']for m in g['moves']]==['WATERFALL','OUTRAGE','CRUNCH','DRAGONDANCE']
print('NORMAL OUTRAGE TUTOR VERIFIED',flush=True)
