"""Clear only expected learning/payment messages, stopping at the overworld."""
from play import *
import re
settled=0
for _ in range(24):
 t=read();print(t,flush=True);low=re.sub('[^a-z]','',t.lower())
 if low in ['', 'pokemonreborn']:
  settled+=1
  if settled<3:act('wait:.6');continue
  break
 settled=0
 if any(re.fullmatch(r'and\.*',line.strip().lower()) for line in t.splitlines()) or any(z in low for z in ['handedoveroneheart','comeagain','learned','forgot','andpoof','machineand']):act('c','wait:.6')
 else:break
else:raise SystemExit('Relearner completion message limit')
