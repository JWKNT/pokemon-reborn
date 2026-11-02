"""Reach Aegir via Charous and the normal descending waterfall; no battle trigger."""
from play import *
def run(s,*a):
 print('AEGIR TRAVEL',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
from locate import locate
assert locate(852)==(852,11,86)
run('surface_walk',852,4,95,'--hold-straights');run('eventq',852,3,'enter')
run('aegir_event',849,54,'enter')
run('teach_machine','TM80','Rayquaza','Rock Slide',1)
run('teach_machine','TM17','Rayquaza','Protect',3)
run('checkpoint','Aegir370-Arrived')
