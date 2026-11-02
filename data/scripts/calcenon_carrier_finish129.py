"""Resume ONLY the visibly reviewed Tranquill Fly menu after completed PC swap."""
import os
os.environ['REBORN_COORD_CACHE']='1'
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
t=read().lower()
assert 'tranquill' in t and 'summary' in t and 'switch' in t and 'cancel' in t, 'Reviewed carrier menu changed'
act('x','wait:.4','x','wait:.5');t=read().lower()
assert 'bag' in t and 'controls' in t and ('options' in t or 'optione' in t or 'uptions' in t), 'Pause Menu required after carrier inspection'
act('x','wait:.5');run('overworld')
run('eventq',415,8,'enter')
run('checkpoint','Route4-carrier-129')
s=json.loads((ROOT/'notes/Route4-carrier-129-status.json').read_text())
assert s['map']==413 and s['position']==[45,28]
assert s['party'][1]['species']=='TRANQUILL' and 'FLY' in {m['move']for m in s['party'][1]['moves']}
assert s['party'][0]['hp']==s['party'][0]['totalhp']
run('calcenon_agate_queue','--execute','--phase','approach','--party-status',ROOT/'notes/Route4-carrier-129-status.json','--journal',ROOT/'work/calcenon-route4-approach-129.json')
