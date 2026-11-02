"""Restore screen support, remove the training item, then approach Marcello."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
s=json.loads((R/'notes/Postgame381-Silva3-Cap145-status.json').read_text());assert s['party'][5]['species']=='MAGEARNA';assert all(m['level']==145 for m in s['party'])
steps=[('take_held','Mewtwo','Power Anklet'),('city_enter',38,519),('fly_to',527,'--carrier','Rayquaza'),('city_enter',527,826),('city_enter',826,827),('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',2),('pc_exchange_named',20,5,'Cresselia','Magearna','--box',2),('party_front','Mewtwo'),('checkpoint','Mewtwo381-Ready'),('eventq',827,57,'talk')]
p=R/'work/mewtwo381-ready.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n');print('MEWTWO READY',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
print('Review actual Marcello dialogue before continuing; previous interaction missed.',flush=True)
