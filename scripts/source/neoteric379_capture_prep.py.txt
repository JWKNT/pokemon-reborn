"""Save the won boss, use unused normal healing shard, prepare FalseSwipe."""
import json,os,time,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
steps=[('checkpoint','Neoteric379-BossWon'),('eventq',895,112,'enter'),('eventq',895,143,'talk'),('checkpoint','Neoteric379-Healed'),('teach_machine','TM54','Magearna','False Swipe',1),('party_front','Magearna','Amoonguss'),('overworld',),('checkpoint','Neoteric379-CaptureReady')]
p=R/'work/neoteric379-capture-prep.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review prior interruption'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('CAPTURE PREP',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 if i==3:
  s=json.loads((R/'notes/Neoteric379-Healed-status.json').read_text());assert all(m['hp']==m['totalhp']for m in s['party'])
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
