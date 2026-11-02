"""Select a reviewed reminder move through the normal Circus NPC."""
from play import *
name,move,index,replacement=sys.argv[1:5]
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',355,35,'talk')
run('choose_dialog','Teach one-by-one.|Remember all.|No','Teach one-by-one.','--source',355,35)
for _ in range(5):
 t=read().lower()
 if 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):break
 assert any(z in t for z in ['which pok','klhich pok','khich pok']),t
 act('c','wait:.7')
else:raise SystemExit('Reminder party not reached')
run('party_pick',name,'--single')
for _ in range(5):
 t=read().lower()
 if 'teach which' in t:break
 assert any(z in t for z in ["what'll it be","whatll it be"]),t
 act('c','wait:.7')
else:raise SystemExit('Reminder moves not reached')
run('relearn_select',move,index,replacement)
run('overworld')
