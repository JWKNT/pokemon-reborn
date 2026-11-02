"""Reviewed static connections and Rock Climb event to TM52; ordinary controls."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('FOCUS PICKUP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('connected_walk',564,566)
run('connected_walk',566,568,22,7)
run('q','568,22,7,right:.12,c,wait:1')
run('finish_rock_climb',568,26,9)
run('connected_walk',568,563,1,9)
run('eventq',563,29,'talk')
run('dialog','--limit=8')
run('checkpoint','Pavilion375-FocusBlast')
run('teach_machine','TM52','Darkrai','Focus Blast',1)
run('overworld')
run('teach_machine','TM52','Magearna','Focus Blast',0)
run('overworld')
run('checkpoint','Pavilion375-Coverage')
