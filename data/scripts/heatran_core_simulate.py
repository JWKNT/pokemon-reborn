"""Static-only validation of a crystal route; does not import game input modules."""
from heatran_core_plan import *
import os
os.environ['REBORN_FROZEN_SAVE']=str(R/'backups/Aster-Heatran294-Cal.rxdata')
state={'variables':{'631':4},'switches':{'1693':True,'1692':True,'1695':True}}
pos=[39,32];history=[];seen=set()
for i in range(28):
 v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'870',*map(str,pos),json.dumps(state)],stderr=subprocess.DEVNULL))
 v['events']['31']['x']=107 if pos[0]<90 else 17 # Verified BrothersReady and Hot2 native checkpoints
 signature=(pos[0]<90,tuple(sorted(state['switches'].items())))
 if signature in seen:print('NO NEW PROGRESS; stop for boulder review',flush=True);break
 seen.add(signature)
 cs=candidates(v);print('STATIC',i,pos,'cold',state['switches']['1693'],'candidates',cs,flush=True)
 ex=approach(v,v['events']['101' if pos[0]<90 else '183'])
 if ex:print('EXIT REACHABLE',ex,flush=True);break
 if cs:
  a=cs[0];history.append(a);pos=list(a['approach'])
  for lo,hi,onoff in a['switches']:
   for sw in range(lo,hi+1):state['switches'][str(sw)]=onoff==0
 else:
  cold=pos[0]<90;eid=32 if cold else 34
  a=approach(v,v['events'][str(eid)])
  if not a:print('BLOCKED',flush=True);break
  history.append({'toggle':eid});state['switches']['1693']=not cold;pos=[129,37] if cold else [37,33]
else:print('BOUND REACHED')
(R/'work/294-core-static-route.json').write_text(json.dumps(history,indent=2))
