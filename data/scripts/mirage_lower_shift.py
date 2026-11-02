"""Use a reviewed lower Mirage glass portal through normal Rock Smash controls."""
from play import *
from locate import locate
mid,eid=map(int,sys.argv[1:3]);assert mid in [881,882]
e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))['events'][str(eid)]
assert e['name']=='Glass' and any(c['code']==201 for c in e['list']) and not any('pbFieldDamage' in str(c) for c in e['list'])
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),'talk'],check=True)
for i in range(16):
 t=read().lower();print(t,flush=True)
 if 'yes' in t and 'rock smash' in t:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True);continue
 if 'used rock smash' in t or 'used rock' in t:act('c','wait:1');continue
 assert not any(z in t for z in ['fight','wild','hp','shattered glass hurt']),t
 act('wait:1')
 if i>=2:break
actual=locate();assert actual[0]==1763-mid,('Mirror arrival differs',actual)
print('LOWER MIRROR TRANSFER VERIFIED',actual,flush=True)
