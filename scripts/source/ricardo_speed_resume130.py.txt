"""Reviewed remaining Ricardo hail speed setup; explicit interrupted bag entry."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from play import read,act
v=json.loads((ROOT/'work/ricardo-speed1.json').read_text())
assert v['result']=='helpers_returned' and v['final_classification']=='fresh_expected_command'
hp=v['final_hp_proof']['hp']
for i in range(2,4):
 if hp<93:
  out=ROOT/'work'/('ricardo-speed-heal'+str(i)+'.json')
  subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','1','--item','Ultra Potion','--output',str(out)],check=True)
  r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp'];assert hp>=93
 out=ROOT/'work'/('ricardo-speed'+str(i)+'.json')
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','93','--item','X Speed','--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp']
 messages=' '.join(line for c in r['literal_message_candidates'] for line in c['lines']).lower()
 assert 'used the xspeed' in messages.replace('x speed','xspeed'),'Actual X Speed use receipt required; own stats reviewed after setup'
if hp<200:
 out=ROOT/'work/ricardo-presweep-heal.json'
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','1','--item','Ultra Potion','--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp']
print('SPEED SETUP COMPLETE; STOP FOR ROOT SWEEP REVIEW',hp,flush=True)
