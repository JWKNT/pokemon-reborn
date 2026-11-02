"""Bounded normal-UI Magearna EV blocks, reconciled against ordinary saves."""
import json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_CHUNK='84')
def run(s, *a):
    subprocess.run([sys.executable, str(R/'scripts'/f'{s}.py'), *map(str,a)], check=True)
def saved(label):
    return next(m for m in json.loads((R/'notes'/f'{label}-status.json').read_text())['party'] if m['species']=='MAGEARNA')
def train():
    p=R/'notes/battle-control.json';c=json.loads(p.read_text())
    targets=['Rattata','Bidoof','Patrat','Zigzagoon','Meowth','Pidgey','Noctowl','Persian','Hoothoot','Linoone','Spinarak','Ariados']
    c.update(stop=False,expected_foes=targets)
    p.write_text(json.dumps(c,indent=2)+'\n')
    # Installed weak Opal grass targets: Aura Sphere has20PP and covers the approved normal targets; avoid Raticate Endeavor.
    # Bounded public-UI battles; reconcile exact EVs only after ordinary save.
    run('train_wild_bulk','Magearna',2,8,'--targets',','.join(targets),'--foe-slots',json.dumps({'Spinarak':0,'Ariados':0}),'--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal','--heal-item','Ultra Potion')
def grass():
    run('eventq',38,6,'enter')
    run('q','519,28,51,up:.12,wait:1')
phase=sys.argv[1]
if phase=='hp':
    m=saved('Postgame288-MagearnaTraining')
    assert m['ev']==[0,0,0,0,0,0],m
    run('eventq',38,3,'talk');run('heal')
    run('give_held','Power Weight','Magearna','--single-step')
    grass();train();label='Postgame288-MagearnaHP';expected=[252,0,0,0,0,0]
elif phase=='spa':
    assert saved('Postgame288-MagearnaHP')['ev']==[252,0,0,0,0,0]
    assert saved('Postgame288-MagearnaHP')['moves'][0]['move']=='FLASHCANNON'
    run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
    run('eventq',38,3,'talk');run('heal')
    run('give_held','Power Lens','Magearna','--single-step')
    grass();train();label='Postgame288-MagearnaEV';expected=[252,0,0,252,0,0]
else:raise SystemExit('Use hp or spa')
run('checkpoint',label)
assert saved(label)['ev']==expected,(saved(label)['ev'],expected)
print('VERIFIED MAGEARNA EV',label,expected,flush=True)
