"""Normal controls for a bounded, saved-EV-verified two-participant training plan."""
import subprocess,sys,json,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
TARGETS='Noibat,Woobat'
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=R)
def checkpoint(label,swamp_ev,arca_ev):
 run('checkpoint',label)
 st=json.loads((R/'notes'/f'{label}-status.json').read_text())
 for species,expected in [('SWAMPERT',swamp_ev),('ARCANINE',arca_ev)]:
  m=next(m for m in st['party'] if m['species']==species)
  assert m['ev']==expected,(species,m['ev'],expected)
 return st
def bulk(n,pair=True):
 a=['Arcanine',1,n,'--targets',TARGETS,'--flex-targets','--ev-ledger']
 if pair:a+=['--hunter','Swampert','--relead-hunter']
 run('train_wild_bulk',*a)
phase=sys.argv[1]
if phase=='prepare':
 run('give_held','Power Weight','Swampert')
 run('give_held','Power Lens','Arcanine')
 run('party_front','Swampert')
 run('eventq',355,118,'talk');run('heal')
 run('fly_to',519,'--carrier','Tranquill')
 run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
 checkpoint('Saphira-pair-training-ready',[32,155,0,0,0,0],[34,0,0,107,0,0])
elif phase=='pilot':
 from play import read,act
 run('hunt_target',TARGETS,'--expire-repel')
 run('battle_batch','Swampert',0,'--foes',TARGETS,'--turns',0)
 t=read().lower();assert 'fight' in t and 'hp' in t,t
 p=R/'notes/current-run-control.json';x=json.loads(p.read_text())
 if not x.get('battle_turbo_enabled',False):
  act('tab','wait:.5');x.update(battle_turbo=True,battle_turbo_enabled=True,battle_turbo_enabled_epoch=time.time(),battle_turbo_evidence='Normal Tab at observed Railnet practice command; fresh game turbo initially off.');p.write_text(json.dumps(x,indent=2)+'\n')
 # Already at a reviewed target; hunter will recognize it without walking.
 # Do not invoke party_front from inside the battle.
 run('train_wild_bulk','Arcanine',1,1,'--hunter','Swampert','--targets',TARGETS,'--flex-targets','--ev-ledger')
 checkpoint('Saphira-pair-training-pilot',[64,155,0,0,0,0],[34,0,0,139,0,0])
elif phase=='weight-lens':
 bulk(int(sys.argv[2]) if len(sys.argv)>2 else 6)
 checkpoint('Saphira-pair-weight-lens-done',[252,155,0,0,0,0],[34,0,0,252,0,0])
elif phase=='bracer-weight':
 run('give_held','Power Bracer','Swampert')
 run('give_held','Power Weight','Arcanine')
 bulk(4)
 checkpoint('Saphira-pair-bracer-weight-done',[252,252,0,0,0,0],[162,0,0,252,0,0])
elif phase=='arcanine-finish':
 run('party_front','Arcanine')
 bulk(3,False)
 checkpoint('Saphira-pair-training-complete',[252,252,0,0,0,0],[252,0,0,252,0,0])
 run('give_held','Wave Incense','Swampert')
 run('give_held','Charcoal','Arcanine')
else:raise SystemExit('Unknown phase')
