"""Normal travel/reminder/TM preparation; verified owned Heart Scale and TM35."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('city_enter',827,826),('city_enter',826,527),('fly_to',521,'--carrier','Rayquaza'),('city_enter',521,116),('onyx_relearn_one','Mewtwo','Recover',14,1),('teach_machine','TM35','Mewtwo','Flamethrower',2),('checkpoint','Mewtwo381-Moves'),('city_enter',116,521),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('checkpoint','Mewtwo381-EVReady')]
p=R/'work/mewtwo381-moves.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n');print('MEWTWO MOVES',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
