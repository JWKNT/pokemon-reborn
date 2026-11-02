"""Continue a completed public-marker search; guarded ordinary capture controls only."""
import os,time,sys,subprocess,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
pid=int(sys.argv[1]);log=R/sys.argv[2]
for _ in range(1000):
 try:os.kill(pid,0)
 except ProcessLookupError:break
 time.sleep(1)
else:raise SystemExit('Search completion timeout; no input sent')
assert 'CONNECTED BERYL MARKER' in log.read_text(),'Search did not find connected marker'
from play import read,act
from ray368_marker import marker
assert 'Reborn Region' in read()
assert marker()['grid']==[1,8]
def run(s,*args):
 print('CAPTURE FOLLOWUP',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],check=True)
run('ray368_grass','--save','Rayquaza368-ThreeMeetings')
t=read().lower()
assert 'rayquaza' in t and ('mawile' in t or 'mamile' in t),t
run('battle_ready')
run('capture_bounded','Mawile','Rayquaza','--ball','Premier Ball','--throws',4,'--total-hp',404,'--heal-below',170)
print('CAPTURE RESULT: inspect before further input',flush=True)
