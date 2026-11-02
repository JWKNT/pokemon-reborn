"""Execute one explicitly reviewed doubles turn, checking each public actor prompt."""
import argparse,json,re,difflib,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('plan',help='JSON list of exactly two actor/slot/target records');a=p.parse_args()
plan=json.loads(a.plan);assert len(plan)==2
active_items={'X Attack','X Defend','X Defense','X Sp. Atk','X Sp. Def','X Speed','X Accuracy','Dire Hit','Guard Spec.'}
# Validate the complete turn before sending its first input.
for step in plan:
 assert isinstance(step.get('actor'),str) and step['actor'].isalpha()
 assert sum(k in step for k in ('switch','item','slot'))==1
 if 'switch' in step:
  assert isinstance(step['switch'],str) and step['switch'].isalpha()
  assert 'target' not in step
 elif 'item' in step:
  assert isinstance(step['item'],str) and step['item'].strip()
  assert isinstance(step.get('on'),str) and step['on'].isalpha()
  assert 'target' not in step and not step.get('mega',False)
  assert step['item'] not in active_items or step['on']==step['actor'], 'X items apply to the acting Pokemon'
 else:
  assert step['slot'] in range(4) and step.get('target') in [None,1,3]
  assert not step.get('mega',False) or step['actor'].lower() in ('mawile','latias','rayquaza')
from play import snap,ROOT
for step in plan:
 rows=snap();text=' '.join(r['text'].lower() for r in rows)
 assert ('fight' in text or 'what will' in text) and re.search(r'\b(?:bag|bae)\b',text),'Public battle command required'
 prompt=' '.join(r['text'].lower() for r in rows if r['x']<.55 and r['y']>.72)
 prompt=re.sub(r'\bmamile\b','mawile',prompt)
 # Directly reviewed native Meowstic prompt OCR on the Endgame battle UI.
 prompt=re.sub(r'\b(?:meaustic|meoustic)\b','meowstic',prompt)
 assert any(difflib.SequenceMatcher(None,step['actor'].lower(),re.sub('[^a-z]','',word)).ratio()>.84 for word in prompt.split()),'Actor changed: '+prompt
 if 'item' in step:
  print('REVIEWED ITEM',step,flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),step['item'],step['on']],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
  continue
 if 'switch' in step:
  assert isinstance(step['switch'],str) and step['switch'].isalpha()
  assert 'slot' not in step and 'target' not in step
  print('REVIEWED SWITCH',step,flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),step['switch']],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
  continue
 assert step['slot'] in range(4) and step.get('target') in [None,1,3]
 cmd=[sys.executable,str(ROOT/'scripts/battle_move.py'),str(step['slot'])]
 if step.get('mega',False):
  assert step['actor'].lower() in ('mawile','latias','rayquaza'), 'Mega plan requires a reviewed eligible Pokemon'
  # Latiasite or Mawilite holders; Rayquaza eligibility requires its prepared Dragon Ascent build.
  cmd.append('--mega')
 if step.get('target') is not None:cmd.append(str(step['target']))
 cmd.append('--watch')
 print('REVIEWED ACTION',step,flush=True);subprocess.run(cmd,check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
print('ONE REVIEWED DOUBLES TURN COMPLETE; reassess public result.',flush=True)
