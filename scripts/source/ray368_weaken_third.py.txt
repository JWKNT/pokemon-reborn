"""Third observed Rayquaza meeting: two safe False Swipes, then one ball."""
from play import *
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
t=read().lower();assert 'rayquaza' in t and ('mawile' in t or 'mamile' in t),t
run('public_turn_capture.py','battle_move.py',1,'--mega','--watch')
t=read().lower();assert 'fight' in t and ('mawile' in t or 'mamile' in t),t
run('public_turn_capture.py','battle_move.py',1,'--watch')
t=read().lower();assert 'fight' in t and ('mawile' in t or 'mamile' in t),t
run('throw_ball.py','Premier Ball')
print('Third capture attempt boundary: inspect result',flush=True)
