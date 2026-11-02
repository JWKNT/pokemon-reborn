"""Bring the already-trained Latias for the five-round sequence; normal UI only."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
s=json.loads((R/'notes/Twilight381-Accepted-status.json').read_text());assert s['party'][2]['species']=='ZAPDOS'
steps=[('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',2),('pc_exchange_named',13,2,'Latias','Zapdos','--box',2),('teach_machine','TM17','Latias','Protect',0),('checkpoint','Twilight381-GauntletReady')]
p=R/'work/twilight381-second-attacker.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n');print('SECOND ATTACKER',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
