"""Reviewed Cascade / Route2 elevator return and nurse, normal UI controls."""
from play import *
from locate import locate
stage=int(sys.argv[1])if len(sys.argv)>1 else 1
def run(n,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(n+'.py')),*map(str,args)],check=True)
if stage<=1:run('surface_event',359,47,'enter')
if stage<=2:
 g=int(json.loads((ROOT/'notes/navigation-state.json').read_text()).get('switches',{}).get('410',False))
 run('layer_walk',360,40,13,g,0,'--hold-straights');act('up:.12','wait:2');assert locate(358)==(358,40,65)
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['switches']['410']=True;p.write_text(json.dumps(s))
if stage<=3:run('layer_walk',358,54,61,1,'--hold-straights');act('right:.12','wait:2');assert locate(365)==(365,4,63)
if stage<=4:
 run('q','365,10,61,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
 run('choose_dialog','Agate Circus|Route 2','Agate Circus');act('c','wait:1')
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['74']=0;p.write_text(json.dumps(s))
 run('q','365,9,51,down:.12,wait:2','365,15,35,right:.12,wait:2')
 assert locate(355)[0]==355
 run('eventq',355,118,'talk');run('heal')
 print('CIRCUS RETURN / FREE NURSE HEAL VERIFIED',flush=True)
