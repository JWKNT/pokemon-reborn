"""Visit three installed mirage shards by normal travel; stop on interruption."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from locate import locate
from play import act
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
# Static maps: every current layout has exactly one shard event69.
allowed=[694,703,704,705]
for i in range(3):
 m,x,y=locate();assert m in allowed,(m,x,y)
 print('MIRAGE',i+1,m,x,y,flush=True)
 subprocess.run([sys.executable,str(R/'scripts/eventq.py'),str(m),'69','enter'],check=True,env=E)
 act('wait:3')
 after=locate();assert after[0]in allowed and after[0]!=m,after
 print('SHARD TRANSITION OBSERVED',after,flush=True)
 # Record only the map transition actually seen, never write native state.
 p=R/'notes/navigation-state.json';d=json.loads(p.read_text())
 d.setdefault('variables',{})['360']=allowed.index(after[0])+1
 d['variables']['359']=i+1
 p.write_text(json.dumps(d,indent=2)+'\n')
subprocess.run([sys.executable,str(R/'scripts/checkpoint.py'),'Postgame243-Mirages'],check=True,env=E)
