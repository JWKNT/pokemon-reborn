"""Restore the battle six through normal PC menus and return to the nurse."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=json.loads((R/'notes/Gyarados182-Supplies-ready-status.json').read_text())
assert s['party'][5]['species']=='TRANQUILL' and s['map']==38

def run(n,*args):
 print('STAGE',n,*args,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1')
 if n in ('eventq','q'):e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,args)],check=True,env=e)

run('give_held','Fairy Gem','Sylveon')
run('eventq',38,6,'enter');run('fly_to',414,'--carrier','Tranquill');run('eventq',414,22,'enter')
run('eventq',772,7,'talk');run('pc_open_reviewed');run('pc_exchange_named',15,5,'Cofagrigus','Tranquill')
run('party_front','Gyarados','Arcanine','Sylveon','Cofagrigus','Swampert','Gigalith')
run('saphira_return_trained');run('checkpoint','Saphira182-Gyarados-ready')
s=json.loads((R/'notes/Saphira182-Gyarados-ready-status.json').read_text())
assert [m['species']for m in s['party']]==['GYARADOS','ARCANINE','SYLVEON','COFAGRIGUS','SWAMPERT','GIGALITH']
assert all(m['level']==95 and m['hp']==m['totalhp'] and not m['status']for m in s['party'])
assert s['party'][0]['item']=='PERSIMBERRY' and s['party'][0]['ev']==[0,252,0,0,0,252]
print('SAPHIRA PARTY VERIFIED; NO BATTLE STARTED',flush=True)
