"""Finite Ricardo hail setup after root one-action pilot; public numeric HP guards."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
prior=json.loads((ROOT/'work/ricardo-pilot2.json').read_text())
assert (prior['result']=='stopped_for_review' and prior['error']=='ValueError: Cropped numeric HUD must independently identify Cofagrigus' and all(h.get('returncode')==0 for h in prior['helpers']))
assert prior['mode']=='ricardo' and prior['explicit_action']['item']=='X Sp.Atk'
from agate_public_action import hp_pair
hp=hp_pair('\n'.join(r['text'] for r in prior['final_rows'] if .37<=r['y']<.70 and r['x']>.5))[0]
assert any('Attackrose sharply' in line for c in prior['literal_message_candidates'] for line in c['lines'])
actions=['X Sp.Atk','X Sp.Atk','X Speed','X Speed','X Speed']
count=1
for item in actions:
 if hp<93:
  count+=1;out=ROOT/'work'/('ricardo-action'+str(count)+'.json')
  subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','1','--item','Ultra Potion','--output',str(out)],check=True)
  r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp'];assert hp>=93
 count+=1;out=ROOT/'work'/('ricardo-action'+str(count)+'.json')
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp','93','--item',item,'--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command';hp=r['final_hp_proof']['hp']
 messages=' '.join(line for c in r['literal_message_candidates'] for line in c['lines']).lower()
 assert ('rose' in messages or 'raised' in messages) and ('sp.' in messages or 'speed' in messages), 'Actual visible boost receipt required'
print('FINITE SETUP COMPLETE; root must review boost receipts and heal before attack',hp,flush=True)
