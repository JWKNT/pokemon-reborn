"""Reviewed Route2 elevator to a previously verified grass strip."""
from play import *
from locate import locate
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('q','355,13,34,left:.12,wait:2','365,8,33,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
run('choose_dialog','Agate Circus|Route 2','Route 2');act('c','wait:.7')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['74']=1;p.write_text(json.dumps(s))
run('q','365,9,51,down:.12,wait:2','365,4,63,left:.12,wait:2')
ground=int(json.loads(p.read_text()).get('switches',{}).get('410',False))
run('layer_walk',358,50,59,ground,0,'--hold-straights')
assert locate(358)==(358,50,59)
print('TRAINING GRASS REACHED',flush=True)
