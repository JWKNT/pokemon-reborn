"""Execute the installed untimed ice puzzle via normal keys and public coordinates."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from locate import *
steps=json.loads((ROOT/'work/250-ice-plan.json').read_text())
assert locate(825)==(825,22,23)
mask=8
for i,s in enumerate(steps):
 act(s['key']+':.12','wait:'+('1.4' if len(s['trail'])>1 else '.10'))
 if s['mask']!=mask:
  if s['mask']==31:act('wait:2');print(read(),flush=True);break
  pos=locate(825);assert pos==(825,*s['end']),(i,s,pos)
  print('ICE CRACK',i,s,flush=True);mask=s['mask']
print('ICE INPUTS COMPLETE; verify quest state',flush=True)
