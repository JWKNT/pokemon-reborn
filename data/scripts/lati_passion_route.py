"""Reviewed post-Joy route through the tower, using only ordinary UI helpers."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(name,*args):
 print('LEG',name,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True)
# The bridge's forced movement is explicit because the ordinary surface
# graph does not model its four-tile crossing.
run('surface_walk.py',857,29,47)
run('play.py','left:.12','wait:2')
run('eventq.py',857,32,'enter')
run('eventq.py',859,35,'enter')
run('eventq.py',859,37,'enter')
run('eventq.py',857,40,'enter')
run('eventq.py',857,41,'enter')
run('eventq.py',857,38,'enter')
run('eventq.py',859,39,'enter')
run('eventq.py',859,41,'enter')
run('eventq.py',857,89,'talk')
run('dialog.py','--limit',45)
