"""Activate a reviewed natural waterfall; verify its observed landing."""
from play import *
from locate import locate
from surface_plan import tag
m,x,y=map(int,sys.argv[1:4]);direction=sys.argv[4];dest=tuple(map(int,sys.argv[5:8]));assert direction in['up','down']
assert locate(m)==(m,x,y)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(x),str(y)],stderr=subprocess.DEVNULL))
front=tag(v,(x,y+(-1 if direction=='up'else 1)))
assert front in ({8} if direction=='up' else {8,9}), 'Expected reviewed waterfall terrain'
# Agate's descending falls use terrain8 without a terrain9 crest. Installed
# HiddenMoves.rb:871 permits normal facingDown+C followed by Waterfall/Yes;
# Field.rb auto-descends only from9. Never replace the transition with a warp.
prompted=direction=='up' or front==8
act(direction+':.12',*(['c','wait:.8']if prompted else ['wait:3']))
t=read();print(t,flush=True)
if prompted and any(re.sub('[^a-z]','',z.lower())in['yes','tes','ves','yee']for z in t.splitlines())and 'no' in t.lower():
 assert 'waterfall' in re.sub('[^a-z]','',t.lower()).replace('haterfall','waterfall')
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
 t=read();assert 'used' in t.lower()and 'waterfall' in re.sub('[^a-z]','',t.lower()).replace('haterfall','waterfall')
 act('c','wait:6')
else:act('wait:4')
actual=locate(dest[0]);assert actual==dest,(actual,dest)
print('WATERFALL ARRIVAL VERIFIED',actual,flush=True)
