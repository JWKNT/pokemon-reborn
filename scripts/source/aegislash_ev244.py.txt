"""Ordinary controlled EV batches, reconciled with an in-game save after each stage."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
phase=sys.argv[1]
e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('AEGISLASH EV',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
def check(label,expected):
 run('checkpoint',label)
 s=json.loads((R/'notes'/f'{label}-status.json').read_text())
 m=next(m for m in s['party'] if m['species']=='AEGISLASH')
 assert m['ev']==expected,(m['ev'],expected)
 print('SAVED OWNED EV VERIFIED',expected,flush=True)
def bulk(n):run('train_wild_bulk','Aegislash',3,n,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--dense-horizontal','--expire-repel')
if phase=='ready':
 snapshot=json.loads((R/'notes/Postgame244-AegisMoves-status.json').read_text())
 mon=next(m for m in snapshot['party'] if m['species']=='AEGISLASH')
 assert mon['level']==110 and mon['ev']==[0,0,0,0,0,0]
 assert [m['move'] for m in mon['moves']]==['SWORDSDANCE','SACREDSWORD','KINGSSHIELD','SHADOWSNEAK']
 run('give_held','Power Weight','Aegislash','--single-step')
 run('party_front','Aegislash')
 # Caller must be outside at the verified Opal Fly landing.
 run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
 check('Postgame244-AegisEVReady',[0,0,0,0,0,0])
elif phase=='pilot':
 bulk(1);check('Postgame244-AegisEVPilot',[32,0,0,0,0,0])
elif phase=='hp':
 bulk(7);check('Postgame244-AegisHPDone',[252,0,0,0,0,0])
elif phase=='attack':
 run('give_held','Power Bracer','Aegislash','--single-step')
 bulk(8);check('Postgame244-AegisEVDone',[252,252,0,0,0,0])
 run('take_held','Aegislash','Power Bracer')
elif phase=='special-defense':
 run('give_held','Power Band','Aegislash','--single-step')
 bulk(1);check('Postgame244-AegisEVFinal',[252,252,0,0,6,0])
 run('take_held','Aegislash','Power Band')
else:raise SystemExit('Unknown EV phase')
