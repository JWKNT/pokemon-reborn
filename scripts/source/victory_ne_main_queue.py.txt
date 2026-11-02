"""Reviewed northeast carts, lever and boulder route via normal controls."""
import json,sys,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];plan=json.loads((R/'work/192-ne-cart-plan.json').read_text())['actions'];start=int(sys.argv[1])if len(sys.argv)>1 else 1;prefix=sys.argv[2]if len(sys.argv)>2 else 'NE193';vars={133:'493',140:'494',141:'495'};switches={134:'1123',136:'1125'}
for i,step in enumerate(plan,1):
 if i<start:continue
 s=json.loads((R/'notes/navigation-state.json').read_text());label=f'{prefix}-{i}'
 if 'event'in step:
  eid=step['event'];assert s['positions']['784'][str(eid)]==[step['box_to'][0]-1,step['box_to'][1]];args=['victory_hazard_boulder_fast.py',str(eid),step['direction'],label]
 else:
  eid=step.get('lever',step.get('cart'))
  if 'cart'in step:assert s['variables'][vars[eid]]==step['before']
  else:assert s['switches'][switches[eid]]!=step['after']
  args=['victory_hazard_interact_fast.py',str(eid),label]
 subprocess.run([sys.executable,str(R/'scripts/hazard_retry.py'),*args],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1'))
 s=json.loads((R/'notes/navigation-state.json').read_text())
 if 'event'in step:assert s['positions']['784'][str(eid)]==step['box_to']
 elif 'cart'in step:assert s['variables'][vars[eid]]==step['after'] and s['positions']['784'][str(eid)]==step['cart_to']
 else:assert s['switches'][switches[eid]]==step['after']
 print('NE ACTION VERIFIED',i,step,flush=True)
assert s['switches']['1126'];print('NE BASEMENT ROCK CLIMB UNLOCKED',flush=True)
