"""Execute a short explicit doubles turn through guarded ordinary controls."""
from play import *
import argparse,difflib
p=argparse.ArgumentParser();p.add_argument('plan');a=p.parse_args()
def norm(x):return re.sub('[^a-z]','',x.lower().translate(str.maketrans({'е':'e','а':'a','о':'o','р':'p','п':'n'}))).replace('mamile','mawile').replace('suampert','swampert').replace('areanine','arcanine').replace('sylueon','sylveon').replace('sylweon','sylveon').replace('sulueon','sylveon').replace('sulveon','sylveon')
for step in json.loads(pathlib.Path(a.plan).read_text()):
 rows=snap();t=' '.join(v['text']for v in rows).lower()
 assert 'fight' in t and re.search(r'\b(?:bag|bae)\b',t),'Battle command menu required'
 prompt=' '.join(v['text']for v in rows if v['y']>.72 and v['x']<.55)
 assert norm(step['actor'])in norm(prompt) or any(difflib.SequenceMatcher(None,norm(step['actor']),norm(w)).ratio()>=.88 for w in prompt.split()),'Actor prompt mismatch: '+prompt
 if step.get('foes'):
  enemy=' '.join(v['text']for v in rows if v['y']<.37)
  assert all(any(difflib.SequenceMatcher(None,norm(n),norm(w)).ratio()>=.8 for w in enemy.split())for n in step['foes']),'Enemy HUD mismatch: '+enemy
 if 'min_hp' in step:
  from public_owned_hp import read as owned_hp
  hp=owned_hp(rows,step['total_hp'])
  assert hp>=step['min_hp'], 'Owned HP guard: '+str(hp)

 cmd=[sys.executable]
 if 'switch'in step:
  cmd += [str(ROOT/'scripts/battle_switch.py'),step['switch']]
 elif 'item'in step:
  cmd += [str(ROOT/'scripts/battle_item.py'),step['item'],step.get('target',step['actor'])]
  if step.get('self_x'):assert step['target']==step['actor']and step['item'].startswith('X ');cmd+=['--active']
 else:
  cmd += [str(ROOT/'scripts/battle_move.py'),str(step['slot'])]
  if 'target'in step:cmd.append(str(step['target']))
  if len(step.get('foes',[]))==2:cmd += ['--foe-names',','.join(step['foes'])]
  if step.get('mega'):cmd+=['--mega']
  cmd+=['--watch']
 subprocess.run(cmd,check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
print('REVIEWED TURN COMPLETE',read(),flush=True)
