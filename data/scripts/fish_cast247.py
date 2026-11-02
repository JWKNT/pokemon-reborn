"""One normal registered-rod cast, reacting only to fresh captured UI text."""
from play import *
from PIL import Image
assert not (ROOT/"notes/fishing247-stop").exists(), "Fishing pause requested before cast"
began=time.time();last='';hooked=False
out=ROOT/'work/fishing247';out.mkdir(exist_ok=True)
act('s:.10')
box=(48,565,229,612)
from PIL import ImageChops,ImageStat
reference=Image.open(ROOT/'work/fishing247/bite-1791452328.182.png').convert('RGB').crop(box)
for i in range(1200):
 h=json.loads((ROOT/'recordings/capture-health.json').read_text())
 assert h.get('active') and time.time()-h['epoch']<2,'Capture stopped'
 im=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')
 delta=sum(ImageStat.Stat(ImageChops.difference(im.crop(box),reference)).mean)/3
 if not hooked and delta<4:
  im.save(out/f'bite-{began:.3f}.png')
  # The framed capture was verified at cast entry. The same timed driver
  # enforces heartbeat, releases the key and logs its timestamps here.
  subprocess.run([KEY,'c:.08'],check=True)
  hooked=True;print('FAST_HOOK',delta,flush=True)
 if not hooked and time.time()-began<10:
  time.sleep(.015);continue
 crop=out/'dialog.png';im.crop((0,480,852,640)).save(crop)
 rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)]))
 t=' '.join(r['text'] for r in rows).lower()
 if t!=last:
  with (out/'casts.jsonl').open('a') as f:f.write(json.dumps({'epoch':time.time(),'cast_start':began,'text':t})+'\n')
  last=t
 if any(s in t for s in ['landed a pok','landedapok']):
  print('LANDED',read(),flush=True);act('c','wait:3')
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
  print('CAST_BATTLE',flush=True);break
 elif any(s in t for s in ['not even','noteven','got away',"use that here"]):
  print('CAST_EMPTY',read(),flush=True);act('c','wait:.5');print(read(),flush=True);break
 elif 'register' in t or 'instant use' in t:raise SystemExit('Registered rod missing')
 time.sleep(.04)
else:raise SystemExit('Cast timed out; inspect screen before more input')
