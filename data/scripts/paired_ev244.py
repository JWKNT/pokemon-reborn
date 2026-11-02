"""Train owned Aegislash and Walrein together through ordinary wild battles."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('PAIRED EV244',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
def check(label,aev,wev):
 run('checkpoint',label);s=json.loads((R/'notes'/f'{label}-status.json').read_text())
 for species,expected in [('AEGISLASH',aev),('WALREIN',wev)]:
  m=next(m for m in s['party'] if m['species']==species)
  assert m['ev']==expected,(species,m['ev'],expected)
 print('PAIRED EV VERIFIED',label,flush=True)
def bulk(n):run('train_wild_bulk','Aegislash',3,n,'--hunter','Walrein','--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--dense-horizontal','--expire-repel','--heal-item','Ultra Potion')
phase=sys.argv[1]
if phase in ['pilot','attack-hp','hp-spdef','finish']:
 (R/'notes/battle-control.json').write_text(json.dumps({'stop':False,'expected_foes':['Noibat','Woobat'],'heal_item':'Ultra Potion'},indent=2))
if phase=='items':
 run('give_held','Power Bracer','Aegislash','--single-step')
 run('give_held','Power Weight','Walrein','--single-step')
 run('party_front','Walrein')
elif phase=='ready':check('Postgame244-PairedEVReady',[0,0,0,0,0,0],[0,0,0,0,0,1])
elif phase=='pilot':
 bulk(1);check('Postgame244-PairedPilot',[0,32,0,0,0,0],[32,0,0,0,0,1])
elif phase=='attack-hp':
 bulk(7);check('Postgame244-PairedAttackHP',[0,252,0,0,0,0],[252,0,0,0,0,1])
elif phase=='hp-spdef':
 run('give_held','Power Band','Walrein','--single-step')
 run('give_held','Power Weight','Aegislash','--single-step')
 bulk(8);check('Postgame244-PairedHPSpDef',[252,252,0,0,0,0],[252,0,0,0,252,1])
elif phase=='finish':
 run('give_held','Power Lens','Walrein','--single-step')
 run('give_held','Power Band','Aegislash','--single-step')
 bulk(1);check('Postgame244-PairedEVFinal',[252,252,0,0,6,0],[252,0,0,5,252,1])
 run('take_held','Aegislash','Power Band');run('take_held','Walrein','Power Lens')
else:raise SystemExit('Unknown paired EV phase')
