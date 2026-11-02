"""Prepare two owned Pokémon for recorded fishing training and move-relearner supplies."""
from play import *
def run(s,*a):
 print('FISH PREP',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('aegir369_fish_ev',5,4)
run('give_held','Power Weight','Rayquaza')
run('aegir369_fish_ev',9,8)
run('checkpoint','Aegir369-RayTrained')
