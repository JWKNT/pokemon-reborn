from nav import *
from locate import locate
def run(s,*a):
 if s=='q':
  f=ROOT/'work/g8-logic-route.json';f.write_text(json.dumps([['q',*a]]));s='safe_steps';a=(f,)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
stage(14)
run('q','305,23,20,up,wait:2','307,13,8,up,wait:2');run('linear_dialog',307,8,'--active');stage(16)
run('eventq',307,14,'talk');run('linear_dialog',307,14,'--active');stage(17)
run('q','307,13,3,up,wait:2','310,7,6,up,wait:2')
for eid,answer,sw in [(12,'Dark',394),(13,'Dark',395),(14,'Light',396)]:
 run('eventq',310,eid,'talk');run('choose_dialog','Light|Dark',answer);run('dialog','--limit=5')
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'][str(sw)]=True;p.write_text(json.dumps(v))
stage(18)
run('q','310,7,21,up,wait:2','308,9,4,up,wait:2')
