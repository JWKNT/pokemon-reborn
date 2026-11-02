"""Finish the third public victory and earn the final candy reward normally."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('FINAL CANDY',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q']:e.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
run('linear_dialog',355,126,'--active','--past-battle','--past-choice');run('trainer_music','finish')
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-Indra-3')
s=json.loads((R/'notes/League221-Indra-3-status.json').read_text());assert s['bag']['contents'].get('EXPCANDYXL')==15
run('league202_candy_rounds',4,1,'League221-Indra-3','League221','--plan',R/'work/session221-indra-plan.json')
run('league203_candy_spend','League221-Indra-4','Mawile','Swablu')
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-NewPair100')
