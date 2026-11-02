"""Normal mint and PC preparation for Glitch Field; no runtime reads or save edits."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('eventq',827,93,'talk'),('bp_store_buy',8,1,'Timid Mint'),('bp_store_exit',),('overworld',),('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',3),('pc_exchange_named',15,5,'Mewtwo','Heatran','--box',3,'--stay-open'),('pc_select_box',2),('pc_exchange_named',20,2,'Zapdos','Cresselia','--box',2),('field_medicine','Timid Mint','Mewtwo'),('overworld',),('take_held','Magearna','Power Weight'),('checkpoint','Mewtwo381-Roster')]
p=R/'work/mewtwo381-prepare.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('PREP381',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
