"""Normal Mawile withdrawal and four reviewed Indra reward rounds."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('CIRCUS PREP',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:e.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=e,check=True)
st=json.loads((R/'notes/League221-SwabluCaught-status.json').read_text());assert st['party'][4]['species']=='SYLVEON'
run('eventq',355,5,'talk');run('pc_open_reviewed');run('pc_exchange_named',16,4,'Mawile','Sylveon')
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-CandyReady')
run('league202_candy_rounds',1,3,'League221-CandyReady','League221','--plan',R/'work/session221-indra-plan.json')
run('league202_candy_rounds',4,1,'League221-Indra-3','League221','--plan',R/'work/session221-indra-plan.json')
run('league203_candy_spend','League221-Indra-4','Mawile','Swablu')
run('eventq',355,118,'talk');run('heal');run('checkpoint','League221-NewPair100')
