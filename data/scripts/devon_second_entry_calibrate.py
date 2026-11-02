"""Return through the powered-down first room, then prove the live radio binding."""
from play import ROOT,act,read
from locate import locate
import sys,json,subprocess

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
run('eventq.py',628,3,'enter');run('eventq.py',628,19,'enter');run('devon_walk.py',630,27,14,'--go','--conveyors')
assert locate(630)==(630,27,14)
act('up:.12','c','wait:.6');print(read(),flush=True)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());assert not s['switches']['749'];s['switches']['749']=True;p.write_text(json.dumps(s))
run('devon_spinners.py','--map',630,'--goal',25,3,'--go');run('eventq.py',630,3,'enter');run('eventq.py',628,4,'enter');run('eventq.py',628,35,'enter')
assert locate(629)[0]==629;act('wait:1');run('checkpoint.py','Devon-second-radio-ready')
before=json.loads(p.read_text());old=before['variables']['342'];assert not before['switches']['745']
act('a:.22','wait:1');run('checkpoint.py','Devon-second-radio-calibrated')
after=json.loads(p.read_text());assert after['variables']['342']==old%3+1,(old,after['variables']['342']);assert not after['switches']['745']
ss=json.loads((ROOT/'notes/Devon-second-radio-calibrated-status.json').read_text());assert all(m['hp']==m['totalhp']for m in ss['party'])
print('NATIVE RADIO CALIBRATION VERIFIED',old,'->',after['variables']['342'],'full HP retained',flush=True)
