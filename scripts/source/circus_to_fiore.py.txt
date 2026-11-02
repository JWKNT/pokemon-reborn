"""Reviewed Route 2 return, stopping outside Fiore instead of descending Waterfall."""
from play import *
from locate import locate
stage=int(sys.argv[1]) if len(sys.argv)>1 else 0
def run(n,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(n+'.py')),*map(str,args)],check=True)
if stage<=0:
 run('use_field_item','Super Repel')
 run('q','355,13,34,left:.12,wait:2','365,8,33,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
 run('choose_dialog','Agate Circus|Route 2','Route 2');act('c','wait:1')
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['74']=1;p.write_text(json.dumps(s))
 run('q','365,9,51,down:.12,wait:2','365,4,63,left:.12,wait:2')
if stage<=1:
 ground=int(json.loads((ROOT/'notes/navigation-state.json').read_text()).get('switches',{}).get('410',False))
 run('layer_walk',358,40,65,ground,'--hold-straights');act('down:.12','wait:2')
 assert locate(360)[0]==360
if stage<=2:
 run('layer_walk',360,11,94,0,'--hold-straights');act('left:.12','wait:2')
 assert locate(359)[0]==359
print('CASCADE / FIORE RETURN VERIFIED; NO MANSION ENTRY YET',flush=True)
