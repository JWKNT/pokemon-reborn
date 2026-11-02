"""Bounded reviewed Blake opening; stop on every unexpected rendered matchup."""
from play import *
import difflib

def run(name,*args):
 return subprocess.call([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)])

def state(actor,foe,offer=False):
 rows=snap();t=' '.join(v['text']for v in rows).lower()
 def has(name,text):
  return any(difflib.SequenceMatcher(None,name.lower(),w.strip('.,!?')).ratio()>=.8 for w in text.split())
 if offer:
  offers=[json.loads(line) for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines() if 'about to send in' in line.lower()]
  latest=offers[-1] if offers else {}
  recent=' '.join(latest.get('text',[])).lower()
  assert ('change pok' in t or 'switch your' in t) and (has(foe,t) or (time.time()-latest.get('epoch',0)<120 and has(foe,recent))),('Expected named free switch',foe,t,recent)
 else:
  own=' '.join(v['text'].lower()for v in rows if v['x']>.5 and .4<v['y']<.71)+' '+' '.join(v['text'].lower()for v in rows if v['y']>.72 and v['x']<.5)
  enemy=' '.join(v['text'].lower()for v in rows if v['y']<.37)
  assert 'fight' in t and has(actor,own) and has(foe,enemy),('Unexpected opening state',actor,foe,t)
 return t

def move(actor,foe,slot):
 state(actor,foe);assert run('battle_move',slot,'--watch')==0
 rc=run('battle_ready')
 if rc:
  t=read().lower();assert 'change pok' in t or 'switch your' in t,t

def switch(actor,foe):
 state(None,foe,True);assert run('battle_switch',actor)==0;assert run('battle_ready')==0;state(actor,foe)
if '--from-weavile' not in sys.argv:
 move('Hexan','Starmie',0)
 move('Hexan','Starmie',3)
 move('Hexan','Starmie',3)
switch('Mienshao','Weavile')
move('Mienshao','Weavile',2)
move('Mienshao','Weavile',3)
switch('Cofagrigus','Mamoswine')
move('Cofagrigus','Mamoswine',0)
print('OPENING COMPLETE: inspect Cofagrigus HP and Trick Room before burn',flush=True)
