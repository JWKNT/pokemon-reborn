"""Read-only simulation of installed Mirage Tower blocks and guide sequences."""
import json,sys,subprocess
from pathlib import Path
from route_readonly import route,ROOT
specs=[(668,23,24,0,'U3 R2'),(670,53,1,1,'U2 L2 D4 R2'),(671,10,32,2,'D L D3 L4 D R D3 R4 D'),(672,49,1,3,'D3 R U R3 D R D2 R'),(674,109,34,4,'R5 D3 R2 D3 R L2 U L4 R3'),(673,92,8,5,'R5 L D6 L3 U4 L D U2')]
plans=[]
for mid,pe,se,stage,seq in specs:
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0',json.dumps({'variables':{'377':stage},'reset_positions':True})],stderr=subprocess.DEVNULL))
 primary=v['events'].pop(str(pe));secondary=v['events'].pop(str(se));v['position']=[-1,-1]
 graph=route(v,None,True);pos=(primary['x'],primary['y']);other=(secondary['x'],secondary['y']);steps=[]
 for token in seq.split():
  key={'U':'up','D':'down','L':'left','R':'right'}[token[0]];n=int(token[1:] or 1)
  for _ in range(n):
   pn=next((dest for k,dest in graph.get(pos,[])if k==key and dest!=other),pos)
   sn=next((dest for k,dest in graph.get(other,[])if k==key and dest!=pn),other)
   steps.append({'direction':key,'primary_before':pos,'primary_after':pn,'secondary_before':other,'secondary_after':sn})
   pos,other=pn,sn
 goals=[c['parameters'][3] for c in primary['list']if c['code']==111 and c['parameters'][:2]in[[1,47],[1,48]]]
 plans.append({'map':mid,'event':pe,'partner':se,'sequence':seq,'steps':steps,'end':[pos,other],'goals':goals,'matched':list(pos)+list(other)==goals})
print(json.dumps(plans,indent=2))
assert all(p['matched']for p in plans),'Source/guide mismatch; do not execute'
