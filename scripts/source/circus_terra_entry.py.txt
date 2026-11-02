"""Restock the reviewed Terra supplies, play the linear reveal, then enter Glitch."""
from play import *
from locate import locate

def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def stage(n,value):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('variables',{})[str(n)]=value;p.write_text(json.dumps(v))
assert locate()[0]==355
run('eventq',355,29,'talk');run('mart_open');run('shop_buy','Cotton Candy',1,5000);run('mart_exit')
run('eventq',355,90,'talk');run('mart_open');run('shop_buy','Hyper Potion',5,1000);run('mart_exit')
run('eventq',355,81,'enter');run('eventq',356,13,'enter')
run('eventq',357,21,'talk');run('linear_dialog',357,21,'--active','--log-scripted-bgm');stage(193,31)
run('eventq',357,15,'talk');run('choose_dialog','Yes|No','Yes')
act('c','wait:2');stage(193,32)
assert locate()[0]==446
print('GLITCH ENTRY VERIFIED',flush=True)
