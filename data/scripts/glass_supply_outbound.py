"""Normal PC exchange for Fly, then leave Glass via the now-working main lift."""
from play import *

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def ground():return int(bool(json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['410']))
if '--espeon-blocks-exit' in sys.argv:
 from locate import locate
 assert locate(732)==(732,35,10)
 act('down:.12','wait:.3','c','wait:2');print(read(),flush=True)
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['947']=True;v['variables'].update({'406':0,'407':0});p.write_text(json.dumps(v))
 q=ROOT/'notes/route-next.json';q.write_text(json.dumps([[732,35,10,34,10,[]],[732,0,0,34,11,[]]]));run('queue_route',q)
 run('glass_companion_wait','Espeon',34,10,'up')
 run('checkpoint','Glass-Espeon-clear-of-exit')
assert not json.loads((ROOT/'notes/navigation-state.json').read_text())['switches'].get('947')
if '--pc-east-ready' not in sys.argv:
 # Main lift opens the front exit; the service entrance reaches the east lift.
 run('layer_walk',732,6,24,ground(),1)
 run('eventq',732,72,'enter');run('eventq',733,66,'talk')
 run('choose_dialog','Ground Floor|B1F|B2F','Ground Floor');run('linear_dialog',733,66,'--active','--past-choice')
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['432']=3;p.write_text(json.dumps(v))
 run('eventq',733,67,'enter');run('eventq',730,3,'enter')
 run('eventq',715,63,'enter');run('eventq',733,20,'enter');run('eventq',733,22,'enter')
run('checkpoint','Glass-east-PC-access')
run('layer_walk',732,70,48,ground())
run('eventq',732,56,'enter');run('eventq',738,3,'talk');run('pc_open_reviewed')
run('pc_exchange_named',12,5,'Tranquill','Klinklang');run('checkpoint','Glass-Fly-supply-party')
run('eventq',738,4,'enter');run('layer_walk',732,70,24,ground(),1)
run('eventq',732,68,'enter');run('eventq',733,7,'enter');run('eventq',733,18,'enter')
print('OUTDOOR GLASS SUPPLY ORIGIN715',flush=True)
