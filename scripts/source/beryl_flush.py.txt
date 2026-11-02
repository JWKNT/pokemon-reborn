"""Reach Titania's installed post-PULSE flush scene through recorded controls."""
from play import *
from locate import locate

def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
if '--from-low' not in sys.argv:
 mid,x,y=locate(496);assert mid==496
 s=json.loads((ROOT/'notes/navigation-state.json').read_text())
 assert s['switches'].get('548') and s['variables'].get('276')==23
 e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'496',str(x),str(y)],stderr=subprocess.DEVNULL))['events']['57']
 assert e['trigger']==1 and (e['x'],e['y'])==(31,22)
 assert {tuple(c['parameters'][1:4])for c in e['list']if c['code']==201}=={(495,29,19)}
 run('layer_walk',496,31,23,int(s['switches'].get('410',False)),0)
 act('up:.12','wait:2')
 run('linear_dialog',496,57,'--active','--burst')
 actual=locate()
 assert actual in [(495,29,19),(505,29,19)],'Flush arrival requires review'
 # The last normal C can activate the button directly above the arrival
 # square after the flush dialogue. Accept only the witnessed clean-high
 # destination, then verify the actual saved water/story state below.
 if actual[0]==495:run('checkpoint','WTC-Beryl-flushed')
if locate()[0]==495:run('wtc_water',495,32,505,'--scene',505,57)
run('checkpoint','WTC-purified')
s=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert s['variables'].get('276')==24 and all(s['variables'].get(str(i))==3 for i in range(256,265))
