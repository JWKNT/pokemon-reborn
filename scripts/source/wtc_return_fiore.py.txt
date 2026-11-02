"""Reviewed purified-water exit and post-WTC Fiore approach, normal input only."""
from play import *
from locate import locate
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
stage=int(sys.argv[1])if len(sys.argv)>1 else 1
if stage<=1:
 s=json.loads((ROOT/'notes/navigation-state.json').read_text())
 assert s['variables'].get('276') in [26,27,28] and all(s['variables'].get(str(i))==3 for i in range(256,265))
 mid,_,_=locate()
 path=[505,504,502,497,467,359]
 assert mid in path,'Unexpected return-route room'
 for dest in path[path.index(mid)+1:]:
  mid,_,_=locate()
  if (mid,dest)==(467,359):run('wtc_waterfall_exit')
  elif (mid,dest)==(497,467):run('wtc_right_exit')
  else:run('wtc_room_exit',mid,dest)
 assert locate(359)[0]==359,'Cascade ascent arrival requires review'
 print('CASCADE ASCENT VERIFIED',flush=True)
if stage<=2:
 run('surface_walk',359,30,27)
 act('up:.12','wait:1')
 run('linear_dialog',359,69,'--follow-source',359,72,'--burst')
 assert locate(359)[0]==359
 run('checkpoint','Fiore-outside-arrival')
 print('FIORE OUTDOOR SCENE VERIFIED; PREPARE BEFORE MANSION ENTRY',flush=True)
