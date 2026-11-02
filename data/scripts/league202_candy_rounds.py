"""Bounded normal Indra wins; verify each five-candy reward in a native save."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1')
 if s in ['eventq','q']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
def saved(label):return json.loads((R/'notes'/f'{label}-status.json').read_text())
start,count=map(int,sys.argv[1:3]);assert 1<=start<=10 and 1<=count<=3
previous=sys.argv[3]
prefix=sys.argv[4] if len(sys.argv)>4 else 'Prep203'
plan=Path(sys.argv[sys.argv.index('--plan')+1]) if '--plan' in sys.argv else R/'work/session202-indra-plan.json'
st=saved(previous);assert st['map']==355
assert any(m['name']=='Arcanine' and m['moves'][1]['move']=='FLAMETHROWER' for m in st['party'])
assert any(m['name']=='Swampert' and m['moves'][0]['move']=='WATERFALL' for m in st['party'])
for matchup in json.loads(plan.read_text())['foes'].values():
 mon=next(m for m in st['party'] if m['name']==matchup['actor'])
 if 'move' in matchup:assert mon['moves'][matchup['slot']]['move']==matchup['move'],matchup
control_path=R/'notes/battle-control.json'
control=json.loads(control_path.read_text());control.update(stop=False,expected_foes=list(json.loads(plan.read_text())['foes']));control_path.write_text(json.dumps(control))
for i in range(start,start+count):
 before=saved(previous)['bag']['contents'].get('EXPCANDYXL',0)
 run('saphira_indra_candy','--turbo','--plan',plan)
 run('eventq',355,118,'talk');run('heal')
 previous=f'{prefix}-Indra-{i}'
 run('checkpoint',previous)
 after=saved(previous)['bag']['contents'].get('EXPCANDYXL',0)
 assert after==before+5,(before,after)
 print('NORMAL CANDY REWARD VERIFIED',i,after,flush=True)
