"""Read short already-recorded battle captions; no game state or native battle logs."""
import argparse, pathlib, subprocess, json, hashlib, concurrent.futures
p=argparse.ArgumentParser();p.add_argument('session',type=int);p.add_argument('start',type=float);p.add_argument('end',type=float);p.add_argument('output',type=pathlib.Path);a=p.parse_args()
assert 0<a.end-a.start<=60
R=pathlib.Path(__file__).resolve().parents[1]
m=json.loads((R/f'recordings/session-{a.session:03}.json').read_text());offset=a.start-m['start_epoch'];assert offset>=0
assert not a.output.exists();a.output.mkdir(parents=True)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(offset),'-i',str(R/m['raw']),'-t',str(a.end-a.start),'-vf','fps=10,crop=852:145:0:490',str(a.output/'%04d.png')],check=True)
# Deduplicate identical caption crops before OCR; each retained image stays reviewable.
seen=set();frames=[]
for f in sorted(a.output.glob('*.png')):
 h=hashlib.sha256(f.read_bytes()).digest()
 if h in seen:continue
 seen.add(h);frames.append(f)
def read(f):
 rows=json.loads(subprocess.check_output([str(R/'scripts/observe'),str(f)]));return {'frame':f.name,'text':' '.join(x['text'] for x in rows)}
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(read,frames))
(a.output/'receipt.json').write_text(json.dumps({'source':'Recorded public video captions only','session':a.session,'start_epoch':a.start,'end_epoch':a.end,'observations':rows},indent=2)+'\n')
last=''
for r in rows:
 if r['text']!=last:print(r['frame'],r['text']);last=r['text']
