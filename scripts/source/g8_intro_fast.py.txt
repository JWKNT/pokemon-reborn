from play import *
from PIL import Image
import re
# Inspected event29312: no choices before Cain's arrival, which is many lines before battle.
for _ in range(40):
 t=read();low=t.lower();print(t,flush=True)
 if 'cain:' in low or 'another guest' in low or re.search(r'\bhp\b|\bfight\b|\bvs\b',low):break
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 if sum(min(p)>210 for p in b.getdata())/(b.width*b.height)>.55:act('c','wait:0.3','c','wait:0.3','c','wait:0.3')
 else:act('wait:1')
else:raise SystemExit('Story guard')
(ROOT/'notes/battle-control.json').write_text('{}')
subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Swampert','1','--foes','muk','--turns','0'],check=True)
