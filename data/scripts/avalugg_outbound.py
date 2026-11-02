"""Reviewed two-dive route from Calcenon to the PULSE; stop before boss interaction."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
run('eventq.py',416,2,'enter');run('eventq.py',413,62,'enter');run('eventq.py',418,5,'enter');run('eventq.py',361,1,'enter')
run('use_field_item.py','Super Repel');run('surface_walk.py',390,37,13)
run('dive_transition.py',390,37,13,392);run('underwater_walk.py',392,14,12)
run('dive_transition.py',392,14,12,390);run('surface_walk.py',390,18,47)
run('dive_transition.py',390,18,47,392);run('underwater_walk.py',392,19,46);run('eventq.py',392,2,'enter')
run('underwater_walk.py',463,19,19);run('dive_transition.py',463,19,19,432);run('surface_walk.py',432,19,13)
run('party_lead.py',1);run('checkpoint.py','preAvalugg')
print('AVALUGG READY — reviewed checkpoint, no battle started',flush=True)
