"""Interpret only installed RPG event switch branches and cart translations.
No live game state access or input. This is an offline route-planning model.
"""
import json

def cart_transition(commands, variable, state, switches, position, directions=False):
 var={variable:state};xy=list(position);active=[True];conditions={};done=False;face=None
 for cmd in commands:
  code,depth,p=cmd['code'],cmd['indent'],cmd['parameters']
  if code==111:
   parent=all(active[:depth+1])
   if p[0]==0:condition=bool(switches[p[1]])==(p[2]==0)
   elif p[0]==1:
    assert p[2]==0 and p[4]==0 and p[1]==variable,p
    condition=var[p[1]]==p[3]
   else:raise ValueError(('Unsupported condition',p))
   active=active[:depth+1]+[parent and condition];conditions[depth]=(parent,condition)
  elif code==411:
   parent,condition=conditions[depth];active=active[:depth+1]+[parent and not condition]
  elif code==412:active=active[:depth+1]
  elif not all(active):continue
  elif code==122:
   if p[0]==variable:assert p[1]==variable and p[2:4]==[0,0];var[variable]=p[4]
  elif code==209:
   if p[0]!=0:continue
   for move in p[1]['list']:
    c=move['code']
    if c in [1,2,3,4]:
     dx,dy={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1)}[c];xy[0]+=dx;xy[1]+=dy;face=(dx,dy)
    elif c not in [0,15,16,17,18,19,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]:raise ValueError(('Unsupported move',move))
 return (var[variable],tuple(xy),face) if directions else (var[variable],tuple(xy))
