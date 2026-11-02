"""Two bounded eight-KO EV blocks using owned Power items and public UI."""
import os,json,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
phase=sys.argv[1];assert phase in ['hp','speed']
label='Mewtwo381-'+('HP' if phase=='hp' else 'EV')
assert not (R/'notes'/f'{label}-status.json').exists()
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
base='Mewtwo381-EVReady' if phase=='hp' else 'Mewtwo381-HP'
m=next(x for x in json.loads((R/'notes'/f'{base}-status.json').read_text())['party']if x['species']=='MEWTWO')
assert m['ev']==([0]*6 if phase=='hp' else [252,0,0,0,0,0]),m['ev']
assert [x['move']for x in m['moves']]==['PSYSTRIKE','RECOVER','FLAMETHROWER','AMNESIA']
if phase=='speed':run('fly_to',519,'--carrier','Rayquaza');run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
run('give_held','Power Weight' if phase=='hp' else 'Power Anklet','Mewtwo','--single-step')
run('party_front','Mewtwo');run('overworld');run('eventq',38,6,'enter');run('q','519,28,51,up:.12,wait:1')
targets=['Raticate','Rattata','Bidoof','Patrat','Zigzagoon','Meowth','Pidgey','Pidgeotto','Noctowl','Persian','Hoothoot','Linoone','Spinarak','Ariados']
(R/'notes/battle-control.json').write_text(json.dumps(dict(stop=False,expected_foes=targets),indent=2)+'\n')
run('train_wild_bulk','Mewtwo',2,8,'--targets',','.join(targets),'--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal','--recover-slot',1,'--recover-below','.6')
run('checkpoint',label)
m=next(x for x in json.loads((R/'notes'/f'{label}-status.json').read_text())['party']if x['species']=='MEWTWO')
assert m['ev']==([252,0,0,0,0,0]if phase=='hp'else[252,0,0,0,0,252]),m['ev']
print('MEWTWO EV VERIFIED',m['ev'],flush=True)
