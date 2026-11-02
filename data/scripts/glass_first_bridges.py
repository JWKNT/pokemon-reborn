"""Reviewed wakeup route and Glaceon ice bridges, then fixed-roster PC prep."""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def state(n,**switches):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=n
 for k,b in switches.items():v['switches'][k]=b
 p.write_text(json.dumps(v))
if '--pc-pending' not in sys.argv:
 run('eventq',733,7,'enter');run('eventq',733,20,'enter')
 p=ROOT/'notes/route-next.json';p.write_text(json.dumps([[733,0,0,27,3,[]]]));run('queue_route',p)
 run('linear_dialog',733,24,'--active','--world-settle',15);state(14)
 run('eventq',733,22,'enter');run('eventq',732,2,'talk')
 run('linear_dialog',732,2,'--active','--world-settle',15);state(15)
 run('eventq',732,3,'talk');run('linear_dialog',732,3,'--active');state(16,**{'939':True})
 run('eventq',732,30,'talk');run('linear_dialog',732,30,'--active','--world-settle',30);state(17,**{'410':False})
run('eventq',732,56,'enter');run('eventq',738,1,'talk');run('dialog','--limit=10')
run('eventq',738,3,'talk');run('pc_open_reviewed');run('pc_exchange_named',12,5,'Klinklang','Tranquill')
run('party_open');t=read();assert 'klink' in t.lower() and 'tranquill' not in t.lower(),t
run('overworld');run('party_front','Arcanine','Klinklang');run('checkpoint','Glass-fixed-six-ready')
run('eventq',738,4,'enter')
run('layer_walk',732,68,38,1,0);run('eventq',732,47,'talk')
run('linear_dialog',732,47,'--active','--burst');state(18,**{'944':True,'945':True})
run('eventq',732,50,'talk');run('linear_dialog',732,50,'--active','--burst');state(19)
print('GLASS FIRST GRUNT LOCKED DOOR; READY TO SMASH SERVER WINDOW',locate(732),flush=True)
