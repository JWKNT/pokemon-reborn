"""Bounded normal-UI Volcanion EV blocks, reconciled against ordinary saves."""
import json, os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_CHUNK='84')
def run(s, *a):
    subprocess.run([sys.executable, str(R/'scripts'/f'{s}.py'), *map(str,a)], check=True)
def saved(label):
    return next(m for m in json.loads((R/'notes'/f'{label}-status.json').read_text())['party'] if m['species']=='VOLCANION')
def train():
    p=R/'notes/battle-control.json';c=json.loads(p.read_text())
    targets=['Rattata','Bidoof','Patrat','Zigzagoon','Meowth','Pidgey','Noctowl','Persian','Hoothoot','Linoone']
    c.update(stop=False,expected_foes=targets)
    p.write_text(json.dumps(c,indent=2)+'\n')
    # Noctowl50's last four installed moves are Air Slash/Uproar/Roost/Moonblast;
    # trained Volcanion's Flamethrower is a safe OHKO without Hypnosis risk.
    # Installed night grass adds Persian25-50, Hoothoot25-50, Linoone45-65.
    # Fire special STAB clears these; retain flee for Raticate's Endeavor loop
    # and the spiders' possible poison while Power Lens slows our attacker.
    run('train_wild_bulk','Volcanion',1,8,'--targets',','.join(targets),'--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal','--heal-item','Ultra Potion')
def grass():
    run('eventq',38,6,'enter')
    run('q','519,28,51,up:.12,wait:1')
phase=sys.argv[1]
if phase=='hp':
    m=saved('Postgame262-VolcanionTraining')
    assert m['ev']==[0,0,0,0,0,0],m
    run('eventq',38,3,'talk');run('heal')
    run('give_held','Power Weight','Volcanion','--single-step')
    grass();train();label='Postgame262-VolcanionHP';expected=[252,0,0,0,0,0]
elif phase=='spa':
    assert saved('Postgame262-VolcanionHP')['ev']==[252,0,0,0,0,0]
    assert saved('Postgame262-VolcanionHP')['moves'][1]['move']=='FLAMETHROWER'
    run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
    run('eventq',38,3,'talk');run('heal')
    run('give_held','Power Lens','Volcanion','--single-step')
    grass();train();label='Postgame262-VolcanionEV';expected=[252,0,0,252,0,0]
else:raise SystemExit('Use hp or spa')
run('checkpoint',label)
assert saved(label)['ev']==expected,(saved(label)['ev'],expected)
print('VERIFIED VOLCANION EV',label,expected,flush=True)
