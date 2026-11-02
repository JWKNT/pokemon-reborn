"""Repeat the installed non-backtracking maze exits via native controls."""
from play import *
from locate import locate
def r(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text())
# First east loop was observed from31,23 to11,28; initial saved361=0.
assert locate(696)==(696,11,28)
s['variables']['380']=1;s['variables']['361']=4;p.write_text(json.dumps(s))
for count in [2,3]:
 r('eventq',696,17,'enter');r('settle_arrival',696)
 assert locate(696)==(696,11,28)
 s=json.loads(p.read_text());s['variables']['380']=count;s['variables']['361']=4;p.write_text(json.dumps(s))
r('eventq',696,100,'enter');r('settle_arrival',697)
s=json.loads(p.read_text());s['switches']['874']=True;p.write_text(json.dumps(s))
r('eventq',697,24,'enter');r('settle_arrival',698)
print('CASTLE ENTRY COMPLETE',flush=True)
