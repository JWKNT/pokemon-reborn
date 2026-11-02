"""Reviewed Grand Hall reward fights and normal candy leveling after EV completion."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
s=json.loads((R/'notes/Mewtwo381-EV-status.json').read_text());m=next(x for x in s['party']if x['species']=='MEWTWO');assert m['ev']==[252,0,0,0,0,252]
steps=[('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('silva367_round','Postgame381-Silva1'),('silva367_round','Postgame381-Silva2'),('silva367_round','Postgame381-Silva3'),('postgame_candy_spend','Postgame381-Silva3',145)]
p=R/'work/mewtwo381-candy.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n');print('MEWTWO CANDY',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
