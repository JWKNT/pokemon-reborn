"""Normal UI training; validate actual frozen EVs at each block."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS="1",REBORN_ROUTE_CHUNK="84",REBORN_COORD_CACHE="1")
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
def check(label,ev):
 run('checkpoint',label)
 m=next(m for m in json.loads((R/'notes'/f'{label}-status.json').read_text())['party'] if m['species']=='AMOONGUSS')
 assert m['ev']==ev,(m['ev'],ev)
 print('AMOONGUSS VERIFIED',m['ev'],m['totalhp'],flush=True)
def bulk(n):run('train_wild_bulk','Amoonguss',3,n,'--targets','Rattata,Bidoof,Patrat,Zigzagoon,Meowth,Pidgey','--flex-targets','--ev-ledger','--expire-repel','--heal-item','Ultra Potion')
phase=sys.argv[1]
if phase=='pilot':
 run('q','519,28,51,up:.12,wait:1');bulk(1);check('Postgame235-AmooHPPilot',[32,0,0,0,0,0])
elif phase=='hp-six':
 bulk(6);check('Postgame235-AmooHP224',[224,0,0,0,0,0])
elif phase=='hp-def':
 run('fly_to',519,'--carrier','Altaria');run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal');run('eventq',38,6,'enter')
 run('q','519,28,51,up:.12,wait:1');bulk(1);check('Postgame235-AmooHP',[252,0,0,0,0,0])
 run('give_held','Power Belt','Amoonguss','--single-step');bulk(6);check('Postgame235-AmooDef192',[252,0,192,0,0,0])
elif phase=='def-six':
 run('give_held','Power Belt','Amoonguss','--single-step');bulk(6);check('Postgame235-AmooDef192',[252,0,192,0,0,0])
elif phase=='finish':
 saved=json.loads((R/'notes/Postgame235-AmooDef192-status.json').read_text())
 mon=next(m for m in saved['party'] if m['species']=='AMOONGUSS')
 if mon['moves'][3]['pp']<6 or mon['hp']<mon['totalhp']*.6:
  run('fly_to',519,'--carrier','Altaria');run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal');run('eventq',38,6,'enter');run('q','519,28,51,up:.12,wait:1')
 bulk(2);check('Postgame235-AmooBulk',[252,0,252,0,0,0])
 run('take_held','Amoonguss','Power Belt')
else:raise SystemExit('Unknown phase')
