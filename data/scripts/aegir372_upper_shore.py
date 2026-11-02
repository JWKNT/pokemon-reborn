"""Normal Dive detour from Aegir lower landing to upper shore; no battle trigger."""
from play import *
def run(s,*a):
 print('AEGIR UPPER SHORE',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('surface_walk',850,26,65,'--hold-straights')
run('dive_transition',850,26,65,851)
run('underwater_walk',851,23,61)
run('eventq',851,3,'enter')
run('underwater_walk',851,43,13)
run('eventq',851,7,'enter')
run('underwater_walk',851,68,107)
run('dive_transition',851,68,107,850)
run('surface_walk',850,68,103,'--hold-straights')
run('eventq',850,57,'enter')
from locate import locate
assert locate(850)==(850,62,33)
