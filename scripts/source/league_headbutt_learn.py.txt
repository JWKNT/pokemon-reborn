"""Finish the ordinary paid Headbutt tutor prompt, verifying named learner."""
from play import *
from learning import PLANS,resolve
for _ in range(6):
 t=read().lower();print(t,flush=True)
 if 'cancel' in t and ('teach which' in t or t.count('hp')>=5):break
 assert any(z in t for z in ['which pok','choose a pok','headbutt','perfect']),t
 act('c','wait:.5')
else:raise SystemExit('Tutor party entry timeout')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),'Swampert','--single'],check=True)
PLANS['headbutt']=2
t=read();print(t,flush=True)
assert 'headbutt' in ''.join(t.lower().split()) and 'swampert' in t.lower(),t
assert resolve(t),'Tutor learning review'
for _ in range(15):
 t=read().lower();print(t,flush=True)
 if all(z in t for z in ['headbutt','bounce','heal bell','bug bite']):act('x','wait:.7');continue
 if 'any time, kid' in t or 'perfect' in t:act('c','wait:.6');continue
 if len(t.splitlines())<2:break
 assert any(z in t for z in ['learned','and','poof','forgot']),t
 act('c','wait:.6')
else:raise SystemExit('Tutor completion review')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'League-HeadbuttLearned'],check=True)
s=json.loads((ROOT/'notes/League-HeadbuttLearned-status.json').read_text())
assert next(m for m in s['party']if m['species']=='SWAMPERT')['moves'][2]['move']=='HEADBUTT'
