"""Two source-reviewed Chrysolia boulders; ordinary push inputs and saved-position proof."""
from nav import *
from locate import locate

eid=int(sys.argv[1]);label=sys.argv[2]
assert eid in [14,6]
old,count={14:((33,38),2),6:((35,25),1)}[eid]
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'238','0','0'],stderr=subprocess.DEVNULL))
e=v['events'][str(eid)]
assert (e['x'],e['y'])==old and e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
assert locate(238)==(238,old[0],old[1]+1)
seq=[]
for j in range(count):
 seq += ['up:.12','wait:.65']
 if j<count-1:seq += ['up:.12','wait:.25']
act(*seq)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert n['positions']['238'][str(eid)]==[old[0],old[1]-count],n['positions']['238'][str(eid)]
print('SPRINGS PUSH VERIFIED',eid,n['positions']['238'][str(eid)],flush=True)
