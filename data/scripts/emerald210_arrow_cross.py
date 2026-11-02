"""Normal arrow bait/dodge, with recorded public frames and endpoint verification."""
from play import *
from locate import locate
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'805,26,54'],check=True,env=dict(os.environ,REBORN_ROUTE_CHUNK='112'))
out=ROOT/'work'/f'emerald-arrow-{int(time.time())}';out.mkdir()
def frame(name):
 shutil.copyfile(ROOT/'recordings/capture-preview.png',out/(name+'.png'))
act('right:.12','right:.12','wait:.6');frame('bait')
act('left:.12','left:.12','wait:1.8');frame('dodged')
act('right:.12','right:.12',*(['up:.12']*15),*(['left:.12']*3),*(['down:.12']*2));frame('crossed')
print('FRAMES',out,flush=True)
print('ENDPOINT',locate(805),flush=True)
