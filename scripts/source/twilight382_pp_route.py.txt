"""Collect two still-available installed PP supplies via normal controls."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
steps=[('city_enter',827,826),('city_enter',826,527),('city_enter',527,529),('eventq',529,13,'item'),('checkpoint','Twilight382-MaxElixir'),('city_enter',529,527),('fly_to',520,'--carrier','Rayquaza'),('city_enter',520,528),('eventq',528,38,'item'),('checkpoint','Twilight382-PPSupplies'),('field_medicine','PP Up','Mewtwo')]
p=R/'work/twilight382-pp-route.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n');print('PP ROUTE',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
print('STOP: inspect PP Up move selection; intended Psystrike slot0.',flush=True)
