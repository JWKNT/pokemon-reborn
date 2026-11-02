"""Native castle story trigger, reviewed right-side passages, first Darma command."""
from play import *
def r(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
f=ROOT/'work/g15-lin-trigger-route.json';f.write_text(json.dumps([[698,0,0,9,18]]))
rc=subprocess.call([sys.executable,str(ROOT/'scripts/queue_route.py'),str(f)]);assert rc in [0,2]
r('linear_dialog',698,23,'--source-page',0,'--burst')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['381']=2;s['switches']['877']=False;s['switches']['878']=True;p.write_text(json.dumps(s))
r('eventq',698,30,'enter');r('settle_arrival',698)
r('room_plan','--maps',698,'--start','698,29,45','--goal','698,41','--output',ROOT/'work/g15-castle-to-Darma.json')
r('room_follow',ROOT/'work/g15-castle-to-Darma.json')
r('trainer_enter',698,41,'KNIGHT','Darma')
r('battle_batch','Excadrill',0,'--foes','Turtonator','--turns',1,'--watch')
