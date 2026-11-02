"""Cross inspected Virizion arrow section with ordinary paced inputs, then verify."""
import json,sys,subprocess,time
from pathlib import Path
from itertools import groupby
from play import act,ROOT
from locate import locate
from route_readonly import route
assert locate(835)==(835,37,28)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'835','37','29',json.dumps({'variables':{'586':4}})],stderr=subprocess.DEVNULL))
path=route(v,(23,48));assert not any(k.startswith('jump:') for k in path),path
journal=ROOT/'work'/f'251-virizion-{int(time.time())}.json'
journal.write_text(json.dumps({'start_epoch':time.time(),'route':path,'source':'installed map geometry, normal public start coordinate'},indent=2))
act('down:.12','wait:1.6')
for key,n in groupby(path):
 seq=[]
 for _ in n:seq.extend([key+':.12','wait:.06'])
 act(*seq)
act('wait:3')
actual=locate(835);assert actual==(835,23,48),actual
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame251-VirizionCleared'],check=True)
s=json.loads((ROOT/'notes/Postgame251-VirizionCleared-navigation.json').read_text());assert s['variables']['586']==6,s['variables']['586']
print('VIRIZION ARROWS COMPLETE',flush=True)
