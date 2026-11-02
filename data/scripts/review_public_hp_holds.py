"""Read-only stable-tail proposals from public recorded HP bars, never runtime.
No inputs, publication, or automatic edit application. Review proposals visually.
"""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('session',type=int);p.add_argument('output',type=Path);a=p.parse_args();assert not a.output.exists();r=Path(__file__).resolve().parents[1]
m=json.loads((r/'recordings'/f'session-{a.session:03}.json').read_text());assert 'stop_epoch' in m
cuts=json.loads((r/'work'/f'session-{a.session:03}-trainer-menu-idle.json').read_text())['intervals'];rows=[]
for i,(start,end)in enumerate(cuts):
 cmd=['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(start),'-t',str(end-start),'-i',str(r/m['raw']),'-vf','fps=2,scale=426:320','-f','rawvideo','-pix_fmt','rgb24','-']
 proc=subprocess.Popen(cmd,stdout=subprocess.PIPE);size=426*320*3;sigs=[]
 while True:
  b=proc.stdout.read(size)
  if not b:break
  assert len(b)==size
  im=np.frombuffer(b,np.uint8).reshape(320,426,3);sig=[]
  for x0,x1,y0,y1 in [(.17,.40,.08,.21),(.17,.40,.21,.37),(.73,.95,.43,.63),(.73,.95,.63,.71)]:
   z=im[int(320*y0):int(320*y1),int(426*x0):int(426*x1)].astype(np.int16);rr,gg,bb=z[:,:,0],z[:,:,1],z[:,:,2];mask=((gg>75)&(gg>rr*1.3)&(gg>bb*1.3))|((rr>130)&(bb<70)&(gg<220));sig.append(int(mask.sum(axis=1).max()))
  sigs.append(sig)
 assert proc.wait()==0 and sigs
 # Earliest suffix matching final HP lengths within one half-resolution pixel.
 last=sigs[-1];changes=[j for j,s in enumerate(sigs)if any(abs(x-y)>1 for x,y in zip(s,last))];tail=start+(max(changes)+1)*.5+1 if changes else start
 rows.append({'index':i,'original':[start,end],'signatures_start_mid_end':[sigs[0],sigs[len(sigs)//2],last],'last_different_hp_time':start+max(changes)*.5 if changes else None,'proposed':[tail,end] if end-tail>=8 else None,'samples':len(sigs),'public_pixels_only':True})
 print(i,rows[-1],flush=True)
a.output.write_text(json.dumps(rows,indent=2)+'\n')
