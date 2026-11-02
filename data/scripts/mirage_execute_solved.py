"""Execute one source-solved puzzle with public block checks and a final save."""
import json,os,sys,subprocess,time,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];idx=int(sys.argv[1]);start=int(sys.argv[2])if len(sys.argv)>2 else 0
plan=json.loads((R/'work/243-mirage-solved.json').read_text())[idx];steps=plan['steps'];assert 0<=start<len(steps)
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('MIRAGE ACTION',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
at=start
for direction,seq in itertools.groupby(steps[start:],lambda z:z['direction']):
 n=len(list(seq));run('mirage_push_group',plan['map'],plan['event'],direction,n,'--plan-start',at);at+=n
 with (R/'work/mirage243-progress.jsonl').open('a')as f:f.write(json.dumps({'epoch':time.time(),'puzzle':idx+1,'next_step':at})+'\n')
label=f'Postgame243-MiragePuzzle{idx+1}';run('checkpoint',label)
n=json.loads((R/'notes/navigation-state.json').read_text());assert n['variables']['377']==idx+1,('Completion variable not set',n['variables'].get('377'))
print('PUZZLE VERIFIED',idx+1,flush=True)
