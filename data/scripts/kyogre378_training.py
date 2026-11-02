"""Two bounded normal-UI EV blocks with ordinary-save reconciliation."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
def saved(label):return next(m for m in json.loads((R/'notes'/f'{label}-status.json').read_text())['party'] if m['species']=='KYOGRE')
phase=sys.argv[1];assert phase in ['hp','spa']
label='Neoteric378-Kyogre'+('HP' if phase=='hp' else 'EV')
assert not (R/'notes'/f'{label}-status.json').exists(),'Already completed; inspect latest save'
if phase=='hp':
 assert saved('Postgame378-Silva4')['ev']==[0,0,0,0,0,0]
 run('teach_machine','TM55','Kyogre','Scald',2)
else:
 assert saved('Neoteric378-KyogreHP')['ev']==[252,0,0,0,0,0]
 run('fly_to',519,'--carrier','Rayquaza');run('eventq',519,116,'enter')
run('eventq',38,3,'talk');run('heal')
run('give_held','Power Weight' if phase=='hp' else 'Power Lens','Kyogre','--single-step')
run('party_front','Kyogre');run('overworld')
run('eventq',38,6,'enter');run('q','519,28,51,up:.12,wait:1')
targets=['Rattata','Bidoof','Patrat','Zigzagoon','Meowth','Pidgey','Noctowl','Persian','Hoothoot','Linoone','Spinarak','Ariados']
p=R/'notes/battle-control.json';p.write_text(json.dumps(dict(stop=False,expected_foes=targets),indent=2))
run('train_wild_bulk','Kyogre',2,8,'--targets',','.join(targets),'--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal','--heal-item','Ultra Potion')
run('checkpoint',label)
expected=[252,0,0,0 if phase=='hp' else 252,0,0]
assert saved(label)['ev']==expected,(saved(label)['ev'],expected)
print('VERIFIED KYOGRE EV',label,expected,flush=True)
