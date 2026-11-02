"""Read public coordinates, then freeze in Party before OCR/planning.
Only captured pixels and ordinary controls; no live process or game data reads.
"""
from play import *

def party_position():
 t=read().lower();assert 'cancel' in t and t.count('hp')>=5,t
 act('x','wait:.8','x','wait:.2','d:1.0','wait:.3')
 epoch=time.time()
 for _ in range(30):
  h=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if h.get('active') and h.get('preview_epoch',0)>=epoch and time.time()-h['epoch']<2:break
  time.sleep(.1)
 else:raise SystemExit('No fresh coordinate frame')
 dest=ROOT/'work/hazard-coordinates.png';shutil.copyfile(ROOT/'recordings/capture-preview.png',dest)
 act('c:.2','wait:.55','x','wait:.65','c','wait:1.0')
 rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(dest)]));text=' '.join(r['text'] for r in rows)
 print('PUBLIC COORDINATES',text,flush=True)
 m=re.search(r'X\s*(\d+)\s*[,.;]?\s*Y[\s\x27\u2019]*(\d+)\s*[,.;]?\s*map\s*(\d+)',text,re.I)
 t=read().lower();assert 'cancel' in t and t.count('hp')>=5,t
 assert m,'Coordinate review required'
 x,y,mid=map(int,m.groups());return mid,x,y

if __name__=='__main__':print(party_position())
