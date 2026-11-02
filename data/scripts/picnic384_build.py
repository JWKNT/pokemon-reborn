"""Return after both saved captures using normal menus; accept the desert follow-up."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('city_enter',527,826),('city_enter',826,827),('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',2),('pc_exchange_named',20,1,'Magearna','Zygarde','--box',2,'--stay-open'),('pc_select_box',4),('pc_exchange_named',3,0,'Darkrai','Cresselia','--box',4),('teach_machine','TM91','Magearna','Flash Cannon',0),('teach_machine','TM04','Kyogre','Calm Mind',2),('party_front','Magearna'),('checkpoint','Picnic384-BattleTeam')]
p=R/'work/picnic384-build.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('PICNIC BUILD384',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
