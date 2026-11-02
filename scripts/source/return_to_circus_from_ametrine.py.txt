"""Reviewed reverse mountain route from healed Ametrine Center to the Circus."""
from play import *
from locate import locate

def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
if '--outside' not in sys.argv and '--from-366' not in sys.argv:
 run('eventq',458,8,'enter')
 run('use_field_item','Super Repel')
if '--from-366' not in sys.argv:
 run('surface_event',439,2,'enter')
 run('surface_event',373,12,'enter')
run('surface_event',366,22,'enter')
run('surface_event',364,15,'enter')
run('eventq',361,69,'enter')
run('layer_walk',358,54,61,0)
run('q','358,54,61,right:.12,wait:2','365,10,61,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
run('choose_dialog','Agate Circus|Route 2','Agate Circus')
act('c:.12','wait:1')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['74']=0;p.write_text(json.dumps(v))
run('q','365,9,51,down:.12,wait:2','365,15,35,right:.12,wait:2')
assert locate()[0]==355
print('CIRCUS RETURN VERIFIED',flush=True)
