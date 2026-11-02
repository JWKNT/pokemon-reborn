import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('FLY PREP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('overworld')
run('teach_machine','TMX2','Rayquaza','Fly',1)
run('overworld')
run('fly_to',564,'--carrier','Rayquaza')
run('pavilion375_focus_pickup')
