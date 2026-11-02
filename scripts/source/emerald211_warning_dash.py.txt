"""Time ordinary movement against pixels in the recorded warning animation."""
from play import *
from locate import locate
import numpy as np
from PIL import Image
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'805,26,54'],check=True,env=dict(os.environ,REBORN_ROUTE_CHUNK='112'))
out=ROOT/'work'/f'emerald-warning-{int(time.time())}';out.mkdir()
def red():
 a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')).astype(float)
 return int(((a[:,:,0]>90)&(a[:,:,0]>a[:,:,1]*1.45)&(a[:,:,0]>a[:,:,2]*1.15)).sum())
# Validate framing and usage once for this bounded reactive sequence.
# Every key still checks the recorder heartbeat and writes its action log.
act()
def send(*keys):subprocess.run([KEY,*keys],check=True)
send('right:.3')
t=time.time();observed=[]
while time.time()-t<3:
 n=red();observed.append([time.time(),n])
 if n>10000:break
 time.sleep(.04)
else:raise SystemExit('Warning not observed')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'warning.png')
send('left:.3')
t=time.time()
while time.time()-t<3:
 n=red();observed.append([time.time(),n])
 if n<4000:break
 time.sleep(.04)
else:raise SystemExit('Warning did not clear')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'cleared.png')
send('right:.21','up:1.5','left:.3','wait:1.5')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'result.png')
(out/'samples.json').write_text(json.dumps(observed))
print('FRAMES',out,flush=True);print('ENDPOINT',locate(805),flush=True)
