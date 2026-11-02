"""Verified normal checkpoint and curated first Lele attempt entry."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LELE ENTRY',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('party_front','Volcanion','Magearna');run('checkpoint','Bulu305-Ready')
(R/'notes/battle-control.json').write_text(json.dumps({'stop':False,'expected_foes':['Ferrothorn','Gengar','Roserade','Salazzle','Zangoose','Bulu']},indent=2))
run('major_attempt','start',R/'work/major-181.json',305,'--status',R/'notes/Bulu305-Ready-status.json')
run('trainer_enter',855,17,'TAPUBULU','Tapu-Bulu')
