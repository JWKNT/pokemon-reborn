"""One bounded Prisma beam attempt using normal keys and recorded public frames."""
import os
os.environ.setdefault('REBORN_FAST_KEYS','1')
os.environ.setdefault('REBORN_COORD_CACHE','1')
from nav import ROOT,act,read,route
from locate import locate
import json,subprocess,sys,time,threading
from PIL import Image
n=json.loads((ROOT/'notes/navigation-state.json').read_text())
mode=sys.argv[1] if len(sys.argv)>1 else 'green'
assert mode in ['green','dual','triple','final']
assert n['positions']['896']['75']==([26,64] if mode=='final' else [22,61])
assert n['positions']['896']['74']==([17,64] if mode=='green' else [18,64])
assert all(n['switches'][str(k)] for k in [1890,1900,1902])
expected_shadows={'green':[18,64,17,64],'dual':[18,63,17,63],'triple':[18,63,17,63],'final':[26,64,26,68]}
assert [n['variables'][str(k)] for k in [731,732,737,738]]==expected_shadows[mode]
if mode=='triple':
 assert n['positions']['896']['73']==[27,64]
 assert [n['variables'][str(k)] for k in [735,736]]==[26,62]
if mode=='final':
 assert n['positions']['896']['73']==[23,68]
 assert n['positions']['896']['72']==[22,62]
 assert n['positions']['896']['95']==[19,60]
 assert [n['variables'][str(k)] for k in [733,734,735,736]]==[19,60,27,62]
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'896,22,63'],check=True)
assert locate(896)==(896,22,63)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'896','22','63'],stderr=subprocess.DEVNULL))
steps=(['right']*3+['down']*3+['right']+['down']*2) if mode=='final' else (['right']*4+['down']*4+['right'])
point=(22,63)
for d in steps:
 dx,dy={'right':(1,0),'down':(0,1)}[d];after=(point[0]+dx,point[1]+dy)
 assert route(dict(v,position=list(point)),after)==[d]
 point=after
assert point==((26,68) if mode=='final' else (27,67))
out=ROOT/'work'/('prisma-'+mode+'-public-'+str(int(time.time())));out.mkdir()
stop=threading.Event()
def capture():
 last=0
 while not stop.is_set():
  try:
   h=json.loads((ROOT/'recordings/capture-health.json').read_text())
   if h.get('active') and h.get('preview_epoch',0)>last and time.time()-h['epoch']<2:
    last=h['preview_epoch'];im=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB');im.save(out/f'{last:.3f}.png')
  except (OSError,ValueError):pass
  stop.wait(.12)
t=threading.Thread(target=capture);t.start()
try:
 seq=['down:.12','c','wait:.25']
 for d in steps:seq.extend([d+':.12','wait:.1'])
 seq.extend(['right:.12' if mode=='final' else 'down:.12','c','wait:.5'])
 start=time.time();act(*seq)
 text=read();print(text,flush=True)
 assert 'reacted' in text.lower(),'Purple activation needs public review'
 act('c','wait:7');print(read(),flush=True)
 (out/'attempt.json').write_text(json.dumps(dict(start=start,end=time.time(),keys=seq,public_text=text),indent=2))
finally:
 stop.set();t.join()
print('PUBLIC PULSE FRAMES',out,flush=True)
