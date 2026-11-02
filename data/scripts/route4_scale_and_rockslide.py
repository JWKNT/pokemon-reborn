"""Normal Route4 hidden scale pickup, Circus reminder, and return to first climb."""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--reminder-party' not in sys.argv:
 run('eventq',710,64,'item');run('dialog','--limit=10')
 run('fly_to',355);run('eventq',355,35,'talk')
 run('choose_dialog','Teach one-by-one.|Remember all.|No','Teach one-by-one.','--source',355,35)
for _ in range(4):
 t=read().lower();print(t,flush=True)
 if 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):break
 assert any(z in t for z in ['which pok','klhich pok','khich pok']),('Relearner party intro review',t)
 act('c','wait:.7')
else:raise SystemExit('Relearner party entry limit')
run('party_pick','Excadrill','--single')
for _ in range(4):
 t=read().lower();print(t,flush=True)
 if 'teach which' in t:break
 assert any(z in t for z in ["what'll it be","whatll it be"]),('Relearner list intro review',t)
 act('c','wait:.7')
else:raise SystemExit('Relearner list entry limit')
# Installed natural list, duplicate and known-move filtering reviewed: RockSlide11.
run('relearn_select','Rock Slide',11)
run('overworld');run('checkpoint','Glass-RockSlide-ready')
run('fly_to',413);run('eventq',413,21,'enter');run('eventq',418,2,'enter')
run('eventq',412,1,'talk');run('dialog','--limit=10')
assert locate(710)[0]==710
print('ROCKSLIDE PREP COMPLETE; UPPER ROUTE4 RETURN VERIFIED',flush=True)
