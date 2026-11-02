"""Pure read-only model of installed deterministic WTC water-control commands.

Returns a hypothetical navigation snapshot; never sends input or edits the game.
"""
import json, subprocess, pathlib, copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
def predict(source,old,eid,map_loader=None):
 state=copy.deepcopy(source);direction=8
 vars=state.setdefault('variables',{});switches=state.setdefault('switches',{})
 positions=state.setdefault('positions',{});current=old;budget=0
 commons=json.loads((ROOT/'work/wtc-common-model.json').read_text())
 def value(i):return vars.get(str(i),0) or 0
 def mapdata(mid):
  if map_loader:return copy.deepcopy(map_loader(mid,vars,switches,mid!=old))
  extra=json.dumps({'variables':vars,'switches':switches,'reset_positions':mid!=old})
  return json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0',extra],stderr=subprocess.DEVNULL))
 maps={old:mapdata(old)}
 positions.setdefault(str(old),{})
 for k,e in maps[old]['events'].items():positions[str(old)].setdefault(k,[e['x'],e['y']])
 commands=maps[old]['events'][str(eid)]['list']
 def condition(a):
  if a[0]==0:return bool(switches.get(str(a[1]),False))==(a[2]==0)
  if a[0]==1:
   lhs=value(a[1]);rhs=a[3] if a[2]==0 else value(a[3])
   return [lhs==rhs,lhs>=rhs,lhs<=rhs,lhs>rhs,lhs<rhs,lhs!=rhs][a[4]]
  if a[:2]==[6,-1]:return direction==a[2]
  raise RuntimeError('Unsupported control condition '+str(a))
 def execute(cs):
  nonlocal current,budget
  active={-1:True};tested={};loops=[];i=0
  while i<len(cs):
   budget+=1
   if budget>20000:raise RuntimeError('Control model instruction limit')
   c=cs[i];code,a,indent=c['code'],c['parameters'],c['indent']
   if code==111:
    ok=condition(a);tested[indent]=ok;active[indent]=active.get(indent-1,True) and ok
   elif code==411:active[indent]=active.get(indent-1,True) and not tested[indent]
   elif code==412:active.pop(indent,None)
   elif active.get(indent-1,True):
    if code==112:loops.append((i,indent))
    elif code==413:
     assert loops and loops[-1][1]==indent
     i=loops[-1][0]+1;continue
    elif code==113:
     start,level=loops.pop();end=next(j for j in range(i+1,len(cs)) if cs[j]['code']==413 and cs[j]['indent']==level)
     for k in list(active):
      if k>=level:active.pop(k)
     i=end+1;continue
    elif code==117:
     assert str(a[0]) in commons
     execute(commons[str(a[0])]['list'])
    elif code==122:
     if a[3]==0:rhs=a[4]
     elif a[3]==1:rhs=value(a[4])
     elif a[3]==6:
      assert a[5] in [0,1]
      rhs=positions[str(current)][str(a[4])][a[5]]
     else:raise RuntimeError('Unsupported control operand '+str(a))
     for k in range(a[0],a[1]+1):
      lhs=value(k)
      if a[2]==0:result=rhs
      elif a[2]==1:result=lhs+rhs
      elif a[2]==2:result=lhs-rhs
      else:raise RuntimeError('Unsupported control operation '+str(a))
      vars[str(k)]=result
    elif code==121:
     for k in range(a[0],a[1]+1):switches[str(k)]=a[2]==0
    elif code==201:
     assert a[0]==0
     current=a[1];maps[current]=mapdata(current)
     positions[str(current)]={k:[e['x'],e['y']] for k,e in maps[current]['events'].items()}
    elif code==202:
     assert a[1] in [0,1]
     positions[str(current)][str(a[0])]=a[2:4] if a[1]==0 else [value(a[2]),value(a[3])]
    elif code==115:return
    elif code not in [0,108,408,106,223,250]:raise RuntimeError('Unsupported control command '+str(c))
   i+=1
 execute(commands)
 return state,current,budget
