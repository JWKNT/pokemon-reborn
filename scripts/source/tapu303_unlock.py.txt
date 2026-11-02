"""Use the owned Fennekin's Psychic Terrain against the installed level1 Unown."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LELE UNLOCK',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
(R/'notes/battle-control.json').write_text(json.dumps({'stop':False,'expected_foes':['Unown']},indent=2))
run('eventq',855,12,'talk');run('battle_ready')
run('battle_move',3,'--watch');run('battle_ready')
run('battle_move',1,'--watch')
print('CHECK PUBLIC FINISH AND GATE TRANSFER; no automatic trainer entry.',flush=True)
