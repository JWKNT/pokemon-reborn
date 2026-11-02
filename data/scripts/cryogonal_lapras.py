"""Bounded, UI-only Recover/Freeze-Dry policy for the reviewed Lapras matchup."""
from play import *
from PIL import Image
for turn in range(20):
 t=read().lower()
 if 'lapras' not in t or 'fight' not in t or 'what will' not in t and 'ahat will' not in t:
  print('MATCHUP/TRANSITION REVIEW',t,flush=True);break
 im=Image.open(STATE).convert('RGB');w,h=im.size
 pixels=[im.getpixel((x,int(h*.591))) for x in range(int(w*.761),int(w*.929))]
 hp=sum((g>75 and g>r*1.4 and g>b*1.4) or (r>130 and b<70 and g<180) for r,g,b in pixels)/len(pixels)
 slot=2 if hp<.62 else 3
 print('LAPRAS TURN',turn+1,'HP',round(hp,2),'Recover' if slot==2 else 'Freeze-Dry',flush=True)
 r=subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'hexan',str(slot),'--foes','lapras','--turns','1'],capture_output=True,text=True)
 with (ROOT/'work/g6-lapras-policy.log').open('a') as f:f.write(r.stdout+r.stderr)
 if r.returncode or any(s in r.stdout for s in ['REVIEW','no PP','no pp']):
  print(r.stdout[-1800:],r.stderr,flush=True);break
