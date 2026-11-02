"""Normal cart interaction with a destination predicted from installed puzzle source."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];eid=int(sys.argv[1]);label=sys.argv[2];assert eid in [28,29,41,42]
n=json.loads((R/'notes/navigation-state.json').read_text());model=json.loads((R/'work/197-rail-cart-transitions.json').read_text())[str(eid)];var=str(model['variable']);before=n['variables'][var]
if eid==42 and any(n['switches'].get(str(s))for s in [1164,1165]):
 proof=json.loads((R/'work/198-loaded-cart-source-proof.json').read_text());assert len(proof)==2 and all(p['all_80_transitions_match_empty_cart'] and p['player_routes']==0 for p in proof)
mask=sum((1<<i)for i in range(4)if n['switches'].get(str(1160+i)))
pred=next(r for r in model['transitions']if r['before']==before and r['mask']==mask);assert pred['after']!=before,'Cart route unchanged under current switches'
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1'))
run('eventq.py',790,eid,'talk');run('play.py','wait:10');run('checkpoint.py',label)
a=json.loads((R/'notes/navigation-state.json').read_text());assert a['variables'][var]==pred['after'];assert a['positions']['790'][str(eid)]==pred['cart_to'],(a['positions']['790'][str(eid)],pred)
print('RAIL CART VERIFIED',eid,pred,flush=True)
