"""Heal after Mewtwo and stop at Terra's reviewed prebattle position."""
from play import *
from locate import locate
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
assert locate()[0]==454
rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),'454','2','talk'])
if rc and 'cinder' not in read().lower():raise SystemExit('Cinder gate interruption needs review')
run('linear_dialog',454,2,'--active','--burst')
assert locate()[0]==454
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['193']=42;p.write_text(json.dumps(v))
run('eventq',454,6,'talk');run('linear_dialog',454,6,'--active','--burst');run('mark_event',454,6)
run('eventq',454,4,'enter');assert locate()[0]==456
run('party_lead','Swampert');run('q','456,9,6')
run('checkpoint','Mewtwo-won-Terra-prepared')
print('TERRA PREPARATION VERIFIED; safe pause before interaction',flush=True)
