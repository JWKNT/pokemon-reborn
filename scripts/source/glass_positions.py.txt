"""Read-only Glass pallet geometry from installed controller and observed puzzle notes.
Only computes a planner snapshot. Never writes the game or save.
"""
from play import ROOT,json,pathlib

def refresh(v,source):
 variables={int(k):z for k,z in v['variables'].items()};positions={int(k):[e['x'],e['y']] for k,e in source.items()}
 cs=source['64']['pages'][0]['list'];start=next(i for i,c in enumerate(cs)if c['code']==111 and c['parameters'][:2]==[1,408])
 branch={}
 for c in cs[start:]:
  code,indent,a=c['code'],c['indent'],c['parameters']
  parent=all(b for k,b in branch.items()if k<indent)
  if code==111:
   assert a[0]==1,('Unreviewed pallet controller condition',a)
   operand=variables.get(a[3],0)if a[2]else a[3];left=variables.get(a[1],0)
   branch[indent]=parent and [left==operand,left>=operand,left<=operand,left>operand,left<operand,left!=operand][a[4]]
  elif code==411:branch[indent]=parent and not branch[indent]
  elif code==412:branch.pop(indent,None)
  elif parent and code==122:
   assert a[0]==a[1] and a[3]in[0,1,6],a
   if a[3]==0:operand=a[4]
   elif a[3]==1:operand=variables.get(a[4],0)
   else:operand=positions[a[4]][a[5]]
   variables[a[0]]=[operand,variables.get(a[0],0)+operand,variables.get(a[0],0)-operand][a[2]]
  elif parent and code==202:
   eid,mode,x,y,_=a;positions[eid]=[x,y]if mode==0 else[variables.get(x,0),variables.get(y,0)]
 for eid,var in [(63,404),(65,406)]:
  if variables.get(var,0)!=0:positions[eid]=[variables[var],variables.get(var+1,0)]
 v.setdefault('positions',{}).setdefault('732',{}).update({str(eid):xy for eid,xy in positions.items()if source[str(eid)]['name'].startswith('GB') or eid in[63,65]})
 return v
if __name__=='__main__':
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());source=json.loads((ROOT/'work/story-map-732-events.json').read_text());p.write_text(json.dumps(refresh(v,source)))
 print('PLANNER PALLET GEOMETRY REFRESHED FROM OBSERVED STATE',flush=True)
