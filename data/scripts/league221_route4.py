"""Normal Seventh Street exit and previously traversed Route4 approach."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('ROUTE4',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:e.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
run('eventq',324,1,'enter');run('eventq',168,12,'enter');run('eventq',168,18,'talk')
run('choose_dialog','7th Street|Lapis Ward','Lapis Ward');run('dialog','--limit=5');run('checkpoint','League221-SeventhExit')
run('eventq',168,11,'enter');run('eventq',168,2,'enter')
run('fly_to',413);run('eventq',413,21,'enter');run('eventq',418,2,'enter')
run('eventq',412,1,'talk');run('dialog','--limit=10');run('q','710,28,40');run('party_front','Arcanine');run('checkpoint','League221-HeadbuttTree')
