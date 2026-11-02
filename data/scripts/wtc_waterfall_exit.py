"""Use the installed WTC waterfall teleporter through its normal Yes/No UI."""
from play import *
from locate import locate
actual=locate(467);assert actual[0]==467
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'467',*map(str,actual[1:])],stderr=subprocess.DEVNULL))
cs=v['events']['5']['list']
assert any('Kernel.pbWaterfallDialogue' in str(c['parameters'])for c in cs)
assert {tuple(c['parameters'][1:4])for c in cs if c['code']==201}=={(466,15,37)}
subprocess.run([sys.executable,str(ROOT/'scripts/surface_walk.py'),'467','6','9'],check=True)
act('up:.12','c','wait:.8');t=read();print(t,flush=True)
assert re.search('[wh]aterfall',re.sub('[^a-z]','',t.lower()))
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
t=read();print(t,flush=True);assert 'used' in t.lower() and re.search('[wh]aterfall',re.sub('[^a-z]','',t.lower()))
act('c','wait:12')
# The installed waterfall dialogue completes the ascent during this action.
# Event 201 names the intermediate map, but the observed final arrival is 359.
assert locate(359)==(359,26,64)
print('WTC WATERFALL ASCENT TO CASCADE VERIFIED',flush=True)
