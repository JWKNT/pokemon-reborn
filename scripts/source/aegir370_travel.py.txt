"""Reach Aegir via Charous and the normal descending waterfall; no battle trigger."""
from play import *
def run(s,*a):
 print('AEGIR TRAVEL',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('city_enter',38,519);run('fly_to',781,'--carrier','Rayquaza')
# Retain both normal field moves for the descent; reusable TMs restore combat moves.
run('teach_machine','HM03','Rayquaza','Surf',3)
run('teach_machine','HM05','Rayquaza','Waterfall',1)
run('city_enter',781,783);run('city_enter',783,812);run('city_enter',812,785)
run('teach_machine','HM09','Heatran','Rock Climb',3)
run('eventq',785,60,'enter')
run('victory_gem_cliff_event',785,152,'enter',17,52)
run('teach_machine','TM17','Heatran','Protect',3)
run('surface_walk',852,11,44,'--hold-straights')
run('waterfall_step',852,11,44,'down',852,11,86)
run('surface_walk',852,4,95,'--hold-straights');run('eventq',852,3,'enter')
run('aegir_event',849,54,'enter')
run('teach_machine','TM80','Rayquaza','Rock Slide',1)
run('teach_machine','TM17','Rayquaza','Protect',3)
run('checkpoint','Aegir370-Arrived')
