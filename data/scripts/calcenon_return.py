"""Reviewed Circus–Calcenon return after selecting Route 2 in the elevator."""
from play import *
t=read().lower();assert 'now at:' in t and 'route 2' in t,'Route 2 elevator result expected'
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['74']=1;p.write_text(json.dumps(v))
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
def event(mid,eid):run('eventq.py',mid,eid,'enter')
act('c','wait:.7');event(365,24);run('q.py','365,4,63,left,wait:2')
run('layer_walk.py',358,47,13,0);event(358,35)
run('q.py','361,53,17,right,wait:2');event(404,51);event(405,6)
event(404,48);event(409,4);event(408,2);event(410,2);event(409,6)
run('layer_walk.py',404,120,23,1);event(404,45);event(411,6)
event(408,6);event(406,3);event(408,4);event(411,2)
run('q.py','404,169,10,right,wait:2');event(412,22);event(418,1)
print('CALCENON RETURN COMPLETE',flush=True)
