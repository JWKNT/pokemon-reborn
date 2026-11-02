"""Heal owned party through normal PC exchanges, then teach reviewed coverage."""
import os,sys,json,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_FAST_KEYS']='1'
steps=[('pc_select_box',1)]
for i,name in enumerate(['Mewtwo','Amoonguss','Latias','Kyogre','Rayquaza','Cresselia']):
 steps += [('pc_exchange_named',0,i,'Rattata',name,'--box',1,'--stay-open'),('pc_exchange_named',0,i,name,'Rattata','--box',1,*(['--stay-open'] if i<5 else []))]
steps += [('teach_machine','HM03','Latias','Surf',0),('teach_machine','TM04','Mewtwo','Calm Mind',3),('checkpoint','Zygarde383-Healed')]
p=R/'work/zygarde383-heal.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2))
 print('HEAL',i,steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
