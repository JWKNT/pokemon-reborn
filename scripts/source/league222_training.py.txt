"""Paired ordinary EV training with frozen-save verification after every bounded group."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('PAIRED EV',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q']:e.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
def check(label,ma,al):
 run('checkpoint',label);s=json.loads((R/'notes'/f'{label}-status.json').read_text())
 for species,ev in [('MAWILE',ma),('ALTARIA',al)]:
  mon=next(m for m in s['party'] if m['species']==species);assert mon['ev']==ev,(species,mon['ev'],ev)
 print('SAVED EV GAINS VERIFIED',label,flush=True)
def bulk(n):run('train_wild_bulk','Altaria',0,n,'--hunter','Mawile','--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--dense-horizontal','--expire-repel','--heal-item','Full Restore')
phase=sys.argv[1]
if phase=='travel':
 if '--items-ready' not in sys.argv:
  run('give_held','Power Bracer','Mawile','--single-step');run('give_held','Power Weight','Altaria','--single-step')
 run('party_front','Mawile');run('fly_to',519)
 run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
 check('League222-EVReady',[0,0,0,0,0,0],[0,0,0,0,0,0])
elif phase=='pilot':
 bulk(1);check('League222-EVPilot',[0,32,0,0,0,0],[32,0,0,0,0,0])
elif phase=='attack-hp':
 bulk(7);check('League222-AttackHPDone',[0,252,0,0,0,0],[252,0,0,0,0,0])
elif phase=='hp-speed':
 run('give_held','Power Anklet','Altaria','--single-step');run('give_held','Power Weight','Mawile','--single-step')
 run('field_medicine','Max Elixir','Altaria');run('overworld')
 bulk(8);check('League222-EVDone',[252,252,0,0,0,0],[252,0,0,0,0,252])
 run('take_held','Mawile','Power Weight');run('take_held','Altaria','Power Anklet')
else:raise SystemExit('Unknown phase')
