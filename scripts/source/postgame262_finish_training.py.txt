"""Normal healing, two reviewed Friday Will rounds, then owned-candy leveling."""
import json, os, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84',REBORN_WILL_GARDEVOIR_ZAPDOS='1')
s=json.loads((R/'notes/Postgame262-VolcanionEV-status.json').read_text())
m=next(m for m in s['party'] if m['species']=='VOLCANION')
assert m['ev']==[252,0,0,252,0,0] and m['moves'][1]['move']=='FLAMETHROWER'
def run(s,*args):
    print('TRAINING FINISH',s,*args,flush=True)
    subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],check=True)
run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
run('eventq',38,3,'talk');run('heal')
run('take_held','Volcanion','Power Lens')
run('checkpoint','Postgame262-TrainingReady')
for n in [1,2]:run('will_postgame_round',f'Postgame262-Will{n}')
run('postgame_candy_spend','Postgame262-Will2',120)
