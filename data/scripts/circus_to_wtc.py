"""Reviewed Route 2 descent and Waterfall entry, ordinary inputs only.

Stages are restartable after an interruption; every walker observes its endpoint.
The map-466 waterfall animation automatically transfers to map 467.
"""
from play import *
from locate import locate

stage=int(sys.argv[1]) if len(sys.argv)>1 else 0
def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)

if stage<=0:
 run('use_field_item','Super Repel')
 run('q','355,13,34,left:.12,wait:2','365,8,33,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
 run('choose_dialog','Agate Circus|Route 2','Route 2');act('c','wait:1')
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['74']=1;p.write_text(json.dumps(v))
 run('q','365,9,51,down:.12,wait:2','365,4,63,left:.12,wait:2')
if stage<=1:
 ground=int(json.loads((ROOT/'notes/navigation-state.json').read_text()).get('switches',{}).get('410',False))
 run('layer_walk',358,40,65,ground);act('down:.12','wait:2')
 assert locate(360)[0]==360,'Route 2 transfer needs review'
if stage<=2:
 run('layer_walk',360,11,94,0);act('left:.12','wait:2')
 assert locate(359)[0]==359,'Cascade transfer needs review'
if stage<=3:
 run('surface_walk',359,26,64)
 act('down:.03','c','wait:.8');t=read();print(t,flush=True)
 if 'waterfall' not in ''.join(t.lower().split()):raise SystemExit('Waterfall prompt needs review')
 run('choose_dialog','Yes|No','Yes')
 t=read();print(t,flush=True)
 if 'used' not in t.lower():raise SystemExit('Waterfall use needs review')
 act('c','wait:12')
 # Entry automatically lands the player and opens Titania's first linear line.
 if 'titania' in read().lower():run('linear_dialog',467,14,'--burst')
 assert locate(467)[0]==467,'Waterfall arrival needs review'
print('WATER TREATMENT CENTER ARRIVAL VERIFIED',flush=True)
