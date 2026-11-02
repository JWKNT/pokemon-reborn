"""Return from the solved Passion tower and approach Fear through normal UI."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(name,*args):
 print('LEG',name,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True)
for mid,eid in [(857,39),(859,40),(859,43),(857,42),(857,43),
                (857,37),(859,36),(859,31)]:
 run('eventq.py',mid,eid,'enter')
run('surface_walk.py',857,24,47)
run('play.py','right:.12','wait:2')
run('eventq.py',857,35,'enter')
run('eventq.py',859,62,'talk')
run('dialog.py','--limit',45)
