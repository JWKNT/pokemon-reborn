import subprocess,sys,os,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_FAST_KEYS']='1'
steps=[]
for name in ['Magearna','Darkrai','Darkrai','Mewtwo']:
 steps += [('field_medicine','Ultra Potion',name),('overworld',)]
steps += [('teach_machine','TM20','Mewtwo','Safeguard',2),('party_front','Mewtwo'),('checkpoint','Picnic386-EclipseReady')]
p=R/'work/eclipse386-prep-queue.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2))
 print('PREP',i,steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
s=json.loads((R/'notes/Picnic386-EclipseReady-status.json').read_text());assert all(p['hp']==p['totalhp'] and not p['status'] for p in s['party']);assert s['party'][0]['name']=='Mewtwo' and s['party'][0]['moves'][2]['move']=='SAFEGUARD'
