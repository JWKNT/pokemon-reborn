"""Prepare two owned Pokémon for recorded fishing training and move-relearner supplies."""
from play import *
def run(s,*a):
 print('FISH PREP',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',3)
run('pc_exchange_named',15,3,'Rayquaza','Amoonguss','--box',3,'--stay-open')
run('pc_select_box',2);run('pc_exchange_named',25,4,'Arcanine','Mienshao','--box',2)
run('teach_machine','TM46','Arcanine','Thief',0)
run('give_held','Power Bracer','Rayquaza')
run('eventq',38,6,'enter');run('fly_to',232,'--carrier','Zapdos')
run('q','232,16,20,down:.12,wait:.4');run('party_front','Rayquaza')
run('checkpoint','Aegir369-FishingReady')
run('aegir369_fish_ev',1,8)
run('give_held','Power Weight','Rayquaza')
run('aegir369_fish_ev',9,8)
run('checkpoint','Aegir369-RayTrained')
