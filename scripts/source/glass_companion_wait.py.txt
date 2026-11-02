"""Wait an adjacent, visually verified Glass companion using its normal menu.
The companion square is specified from the observed route's final ordinary step.
"""
from play import *
from locate import locate
from glass_positions import refresh
name,x,y,facing=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
assert name in ['Glaceon','Espeon'];p=locate(732)
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[facing]
assert (p[1]+dx,p[2]+dy)==(x,y)
# Verify the actual rendered player facing. A very short CGEvent turn can be
# missed by gameplay polling; repeated guessing can accidentally talk elsewhere.
from sprite_sensor import detect
expected_pose={'down':0,'left':1,'right':2,'up':3}[facing]
if '--facing-ready' not in sys.argv:
 for turn_try in range(6):
  snap();poses=detect(NATIVE,'boy_walk',scale=4)
  if len(poses)!=1:
   # Opaque shading/foreground can defeat exact pixels. Use a bounded sprite
   # match only when its error and direction separation are unambiguous.
   from sprite_match import match
   ranked=match(NATIVE,(1000,740,1280,1010),sprite='boy_walk',zoom=4)
   other=next(z for z in ranked if z[1]!=ranked[0][1])
   assert ranked[0][0]<700 and other[0]>ranked[0][0]*2+100,('Player sprite facing needs visual review',ranked[:5])
   pose={2:0,4:1,6:2,8:3}[ranked[0][1]]
  else:pose=poses[0]['pose'][0]
  if pose==expected_pose:break
  act(facing+':.03','wait:.3')
 else:raise SystemExit('Unable to verify short turning input')
assert locate(732)==p, 'Player moved while turning; review companion position before C' 
act('c','wait:.7');print(read(),flush=True)
opts='Heal Bell|Wait here|Never mind' if name=='Glaceon' else 'Future Sight|Wait here|Never mind'
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),opts,'Wait here'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=6'],check=True)
n=ROOT/'notes/navigation-state.json';v=json.loads(n.read_text());vv=404 if name=='Glaceon' else 406;ss=946 if name=='Glaceon' else 947
v['variables'].update({str(vv):x,str(vv+1):y});v['switches'][str(ss)]=False
n.write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
print('NORMAL WAIT HERE VERIFIED; companion planner',name,x,y,flush=True)
