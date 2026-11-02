"""Reviewed route from Celestinine water entrance to Route 3, through normal UI."""
from play import *
start=int(sys.argv[1]) if len(sys.argv)>1 else 359
assert start in [359,380,430,390]
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
if start==359:
 run('surface_walk.py',359,21,47)
 run('checkpoint.py','pre-mountain')
 act('up:.12','wait:2')
if start in [359,380]:
 run('surface_walk.py',380,52,7)
 run('eventq.py',380,27,'enter')
if start in [359,380,430]:
 run('surface_walk.py',430,32,0)
 act('up:.12','wait:2')
run('surface_walk.py',390,43,37)
run('eventq.py',390,25,'talk')
run('linear_dialog.py',390,25,'--active','--burst')
p=ROOT/'notes/navigation-state.json';state=json.loads(p.read_text());state['variables']['184']=6;p.write_text(json.dumps(state))
run('surface_walk.py',390,96,20)
run('eventq.py',390,15,'enter')
print('MOUNTAIN OUTBOUND COMPLETE — verify Route 3 arrival',flush=True)
