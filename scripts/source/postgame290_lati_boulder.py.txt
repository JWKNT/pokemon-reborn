"""One ordinary leftward Strength push, checked against a frozen checkpoint."""
from play import *
from locate import locate
assert locate(375)==(375,16,32)
def run(n,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('surface_walk',375,15,32)
run('party_open');run('party_pick','Volcanion','--single')
t=read().lower();assert 'strength' in t and 'summary' in t,t
act('down:.12','c','wait:1')
run('dialog','--limit=8');run('overworld')
assert locate(375)==(375,15,32)
act('left:.12','wait:1.5')
run('checkpoint','Postgame290-BoulderOpen')
v=json.loads((ROOT/'notes/Postgame290-BoulderOpen-navigation.json').read_text());assert v['positions']['375']['1']==[12,32],v['positions']['375']['1']
print('BOULDER SLID LEFT TO12,32; NORMAL INPUT VERIFIED',flush=True)
