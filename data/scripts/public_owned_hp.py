"""Read valid owned HP from fresh recorded HUDs; never repair guessed digits."""
import re

def parse(rows,total):
 text=' '.join(v['text'] for v in rows if v['x']>.5 and .4<v['y']<.72)
 values=[int(hp) for hp,maximum in re.findall(r'(\d+)\s*/\s*(\d+)',text)
         if int(maximum)==total and 0<=int(hp)<=total]
 return values[0] if len(values)==1 else None

def read(rows,total):
 from play import snap,STATE,ROOT,subprocess,json
 from PIL import Image
 for attempt in range(5):
  hp=parse(rows,total)
  if hp is not None:return hp
  # Magnify the owned numeric HUD from the same recorded observation.
  # Accept only literal digits and an exact maximum; never infer OCR digits.
  im=Image.open(STATE);w,h=im.size
  crop=ROOT/'work/owned-hp-crop.png'
  im.crop((int(w*.75),int(h*.60),int(w*.96),int(h*.68))).resize((840,320)).save(crop)
  observed=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)]))
  text=' '.join(v['text'] for v in observed)
  values=[int(a) for a,b in re.findall(r'(\d+)\s*/\s*(\d+)',text) if int(b)==total and 0<=int(a)<=total]
  if len(values)==1:return values[0]
  if attempt<4:rows=snap()
 raise AssertionError('Owned HP HUD remained ambiguous after five fresh observations')
