"""Bait the recorded warning beside a narrow corridor, then cross with normal keys."""
from nav import *
from locate import locate
import numpy as np
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'805,27,67'],check=True)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'805','27','67'],stderr=subprocess.DEVNULL));p=route(v,(35,63));seq=[]
for d,g in groupby(p):
 n=len(list(g));seq.extend([d+':.12']*n if n<3 else [d+':'+str(round(.1*n+.02,3))])
print('APPROACH',p,flush=True);act(*seq)
def send(*keys):subprocess.run([KEY,*keys],check=True)
out=ROOT/'work'/f'emerald-corridor-{int(time.time())}';out.mkdir()
t=time.time()
while time.time()-t<9:
 a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')).astype(float)
 a=a[370:600,414:438]; n=int(((a[:,:,0]>70)&(a[:,:,0]>a[:,:,1]*1.4)&(a[:,:,0]>a[:,:,2]*1.1)).sum())
 if n>1700:break
 time.sleep(.04)
else:raise SystemExit('No warning')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'warning.png')
v['position']=[35,63];p=route(v,(36,36));seq=[]
for d,g in groupby(p):
 n=len(list(g));seq.extend([d+':.12']*n if n<3 else [d+':'+str(round(.1*n+.02,3))])
print('DASH50',p,flush=True)
proc=subprocess.Popen([KEY,*seq,'up:.18','c:.12','wait:.2']);j=0
while proc.poll() is None:
 shutil.copyfile(ROOT/'recordings/capture-preview.png',out/f'dash-{j:02}.png');j+=1;time.sleep(.15)
assert proc.returncode==0
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'result.png')
print('FRAMES',out,flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Emerald212-Lever50'],check=True)
