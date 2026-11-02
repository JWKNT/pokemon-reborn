"""Normally collect two source-reviewed uncollected Heart Scales. Stop on wilds."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1')
 if s in ['eventq','q']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
p=sys.argv[1]
if p=='byxbysion':
 run('fly_to',209,'--carrier','Tranquill');run('eventq',209,314,'item');run('checkpoint','Prep202-Byxbysion-scale')
elif p=='scrapyard':
 run('fly_to',693,'--carrier','Tranquill')
 for m,e in [(693,9),(665,31),(665,33),(665,16)]:run('eventq',m,e,'enter')
 run('eventq',691,8,'item');run('checkpoint','Prep202-Scrapyard-scale')
else:raise SystemExit('Unknown phase')
