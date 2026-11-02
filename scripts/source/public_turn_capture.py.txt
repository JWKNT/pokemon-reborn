"""Run a normal UI helper while retaining only already-recorded public text frames."""
import subprocess,sys,time,json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];out=R/'work'/('public-turn-'+str(int(time.time())));out.mkdir()
p=subprocess.Popen([sys.executable,str(R/'scripts'/sys.argv[1]),*sys.argv[2:]])
last=None;count=0;last_saved=None;files=[]
while p.poll() is None:
 try:
  h=json.loads((R/'recordings/capture-health.json').read_text())
  if h.get('active') and time.time()-h['epoch']<2:
   im=Image.open(R/'recordings/capture-preview.png').convert('RGB').crop((15,493,837,628))
   k=hashlib.sha256(im.tobytes()).hexdigest();count=count+1 if k==last else 1;last=k
   if k != last_saved:
    last_saved=k;f=out/f'{time.time():.3f}.png';im.save(f);files.append(f)
 except (OSError,ValueError):pass
 time.sleep(.15)
print("PUBLIC CONTROL COMPLETE",p.returncode,flush=True)
from concurrent.futures import ThreadPoolExecutor
def ocr(f):
 a=json.loads(subprocess.check_output([str(R/'scripts/observe'),str(f)]))
 return f,' '.join(x['text'] for x in a)
rows=[]
pool=ThreadPoolExecutor(max_workers=2)
for f,t in pool.map(ocr,files):
 if t and (not rows or rows[-1]['text']!=t):rows.append({'epoch':float(f.stem),'text':t,'frame':str(f.relative_to(R))});print('PUBLIC TEXT:',t,flush=True)
(out/'text.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(p.returncode)
