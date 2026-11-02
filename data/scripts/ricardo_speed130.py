"""Reviewed remaining Ricardo hail speed setup; explicit interrupted bag entry."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from play import read,act
v=json.loads((ROOT/'work/ricardo-action4.json').read_text())
assert v['result']=='stopped_for_review' and v['helpers'][-1]['returncode']==1
assert 'bag_select.py' in v['helpers'][-1]['stderr']
text=read().lower();assert 'sharply boosts the speed' in text and 'medicine' in text.replace('medieine','medicine')
act('x','wait:.7')
hp=105
for i in range(1,4):
 if hp<93:
  out=ROOT/'work'/('ricardo-speed-heal'+str(i)+'.json')
  subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','1','--item','Ultra Potion','--output',str(out)],check=True)
  r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp'];assert hp>=93
 out=ROOT/'work'/('ricardo-speed'+str(i)+'.json')
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','93','--item','X Speed','--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp']
 messages=' '.join(line for c in r['literal_message_candidates'] for line in c['lines']).lower()
 assert 'speed' in messages and ('rose' in messages or 'raised' in messages),'Visible speed boost required'
if hp<200:
 out=ROOT/'work/ricardo-presweep-heal.json'
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','1','--item','Ultra Potion','--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp']
print('SPEED SETUP COMPLETE; STOP FOR ROOT SWEEP REVIEW',hp,flush=True)
