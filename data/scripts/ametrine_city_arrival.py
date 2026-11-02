"""Reviewed mountain ice route; stop after healing in Ametrine City."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
run('surface_walk.py',366,59,13);run('eventq.py',366,23,'enter')
run('surface_walk.py',373,50,26);run('eventq.py',373,14,'enter')
run('eventq.py',439,58,'talk');run('linear_dialog.py',439,58,'--burst')
run('eventq.py',439,17,'enter')
print('CITY CENTER REACHED; inspect nurse event before continuing',flush=True)
