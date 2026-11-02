"""Reviewed city circuit and abandoned-house scene; stop before Blake's choices."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def variable(k,value):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables'][str(k)]=value;p.write_text(json.dumps(v));print('Observed planning stage',k,value,flush=True)
run('eventq.py',458,8,'enter')
for eid in [32,46]:run('surface_event.py',439,eid,'item')
for eid in [8,4,6]:
 run('surface_event.py',439,eid,'talk');run('linear_dialog.py',439,eid,'--burst');run('mark_event.py',439,eid)
variable(193,6)
for eid in [35,52]:run('surface_event.py',439,eid,'item')
run('surface_event.py',439,18,'enter');run('linear_dialog.py',461,6,'--burst')
variable(193,14);run('eventq.py',461,4,'enter')
run('surface_event.py',439,15,'talk');run('linear_dialog.py',439,15,'--active','--burst')
variable(193,15)
print('AMETRINE INVESTIGATION COMPLETE; Blake refusals pending',flush=True)
