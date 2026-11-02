"""Restore Cresselia, add Mewtwo coverage, and save before boss trigger."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
steps=[('checkpoint','Zygarde383-Gates'),('eventq',846,103,'talk'),('pc_open_reviewed',),('pc_select_box',3),('pc_withdraw_named',19,'Cresselia','--box',3),('teach_machine','TM57','Mewtwo','Charge Beam',2,'--bag-open'),('party_front','Cresselia'),('checkpoint','Zygarde383-Built'),('q','846,51,14'),('checkpoint','Zygarde383-BossEntry')]
p=R/'work/zygarde383-boss-build.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2))
 print('BUILD',i,steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
