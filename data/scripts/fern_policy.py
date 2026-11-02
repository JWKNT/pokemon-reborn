from play import *
import re
plan={'haxorus':('Klinklang',0),'rhydon':('Swampert',2),'krookodile':('Swampert',2),'scyther':('Klinklang',0),'roserade':('Arcanine',1),'decidueye':('Arcanine',1)}
current=sys.argv[1] if len(sys.argv)>1 else 'Klinklang'
for _ in range(10):
 r=snap();t=' '.join(v['text'] for v in r).lower();print(t,flush=True)
 if 'change pok' not in t and 'switch your' not in t:raise SystemExit('Expected free switch')
 # The switch offer may omit the species: recover the latest send-in announcement from this fight.
 name=None
 for l in reversed((ROOT/'recordings/screens.jsonl').read_text().splitlines()[-120:]):
  low=' '.join(json.loads(l)['text']).lower()
  if 'send in' in low or 'sendin' in low:
   name=next((n for n in plan if n in low),None);break
 if not name:raise SystemExit('Opponent review')
 actor,slot=plan[name];print('POLICY',name,actor,slot,flush=True)
 if actor==current:act('x','wait:1.2')
 else:
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),actor],check=True);current=actor
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),actor,str(slot),'--foes',name,'--turns','4','--watch','--min-hp','.28'],check=True)
