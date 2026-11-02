"""Resume after first verified Indra win using the corrected current-moves plan."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('RESUME PREP',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q']:e.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-Indra-1')
s=json.loads((R/'notes/League221-Indra-1-status.json').read_text());assert s['bag']['contents'].get('EXPCANDYXL')==5
run('league202_candy_rounds',2,3,'League221-Indra-1','League221','--plan',R/'work/session221-indra-plan.json')
run('league203_candy_spend','League221-Indra-4','Mawile','Swablu')
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-NewPair100')
