"""Use Opal's east exit, including the installed one-time Shade scene."""
from play import *
from locate import locate
assert locate(497)[0]==497
state=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert state['variables']['276'] in [26,27,28]
def run(n,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(n+'.py')),*map(str,a)],check=True)
if state['variables']['276']==26:
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'497','0','0'],stderr=subprocess.DEVNULL))
 cs=v['events']['19']['list']
 assert any(c['code']==122 and c['parameters']==[276,276,0,0,27]for c in cs)
 run('surface_walk',497,21,4);act('up:.12','wait:1')
 run('linear_dialog',497,19,'--log-scripted-bgm')
 assert locate(497)[0]==497
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['276']=27;p.write_text(json.dumps(s))
 # The first touch plays Shade's message and keeps us on the trigger tile.
 act('down:.12','wait:.5')
run('surface_walk',497,21,4)
act('up:.12','wait:2')
assert locate(467)==(467,13,27)
print('EAST BANK EXIT / SHADE STORY VERIFIED',flush=True)
