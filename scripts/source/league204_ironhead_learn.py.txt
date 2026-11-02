"""Finish the ordinary paid Iron Head tutor prompt, verifying named learner."""
from play import *
from learning import PLANS,resolve
for _ in range(6):
 t=read().lower();print(t,flush=True)
 if 'cancel' in t and ('teach which' in t or t.count('hp')>=5):break
 assert any(z in t for z in ['which pok','choose a pok','iron head','ironhead']),t
 act('c','wait:.5')
else:raise SystemExit('Tutor party entry timeout')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),'Excadrill','--single'],check=True)
PLANS['iron head']=2
t=read();print(t,flush=True)
assert 'ironhead' in ''.join(t.lower().split()) and 'excadrill' in t.lower(),t
assert resolve(t),'Tutor learning review'
for _ in range(15):
 t=read().lower();print(t,flush=True)
 if all(z in t for z in ['knock off','iron head','giga drain','liquidation']):act('x','wait:.7');break
 if 'always a pleasure' in t or "i'll be seeing you" in t:act('c','wait:.6');continue
 if len(t.splitlines())<2:break
 assert any(z in t for z in ['learned','and','poof','forgot']),t
 act('c','wait:.6')
else:raise SystemExit('Tutor completion review')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Prep204-Excadrill-IronHead'],check=True)
s=json.loads((ROOT/'notes/Prep204-Excadrill-IronHead-status.json').read_text())
assert next(m for m in s['party']if m['species']=='EXCADRILL')['moves'][2]['move']=='IRONHEAD'
