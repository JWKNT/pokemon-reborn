"""Bait the recorded warning beside a narrow corridor, then cross with normal keys."""
from nav import *
from locate import locate
import numpy as np
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'805,50,67'],check=True)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'805','50','67'],stderr=subprocess.DEVNULL));p=route(v,(46,64));seq=[]
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
send('left:.12','up:.92','left:.12','up:.82','left:.18','wait:.25')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'alcove.png')
# Lure the next arrow into the one-tile alcove before returning to the corridor.
t=time.time()
while time.time()-t<6:
 a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')).astype(float)[370:600,414:438]
 n=int(((a[:,:,0]>70)&(a[:,:,0]>a[:,:,1]*1.4)&(a[:,:,0]>a[:,:,2]*1.1)).sum())
 if n>1700:break
 time.sleep(.04)
else:raise SystemExit('No alcove warning')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'alcove-warning.png')
def nextwarning(label):
 t=time.time()
 while time.time()-t<6:
  a=np.asarray(Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')).astype(float)[370:600,414:438]
  n=int(((a[:,:,0]>70)&(a[:,:,0]>a[:,:,1]*1.4)&(a[:,:,0]>a[:,:,2]*1.1)).sum())
  if n>1700:break
  time.sleep(.04)
 else:raise SystemExit('No '+label+' warning')
 shutil.copyfile(ROOT/'recordings/capture-preview.png',out/(label+'.png'))
send('right:.12','up:1.02','left:.18','wait:.25')
nextwarning('alcove37')
send('right:.12','up:2.12','left:.12','up:.12','right:.12','wait:.55','right:.12','wait:.2','right:.12','wait:.55','right:.12','wait:.2','right:.12','wait:.55')
shutil.copyfile(ROOT/'recordings/capture-preview.png',out/'result.png')
print('FRAMES',out,flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Emerald212-Plate2'],check=True)
