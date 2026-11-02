from nav import *
goal=tuple(map(int,sys.argv[1:3]))
for attempt in range(12):
 save();v=loadmap();print('POSITION',v['map'],v['position'],'PARTY',[(p['@name'],p['@level'],p['@hp'],p['@totalhp']) for p in v['party']],flush=True)
 if tuple(v['position'])==goal:print('ARRIVED',flush=True);break
 if v['party'][0]['@hp']/v['party'][0]['@totalhp']<.5:print('HEAL NEEDED',flush=True);break
 path=route(v,goal);interrupted=False
 for key,g in groupby(path):
  n=len(list(g));act(f'{key}:{n*.1+.02:.3f}')
  rr=snap()
  if any(a['y']>.73 for a in rr):interrupted=True;print('EVENT',' | '.join(a['text'] for a in rr),flush=True);break
 if interrupted:
  out=subprocess.check_output([sys.executable,str(ROOT/'scripts/train.py'),'80','Cutter','--still','--noswitch'],text=True)
  print(out,flush=True)
  if any(t in out for t in ['REVIEW','MOVE UNKNOWN','LOW HP','TYPE REVIEW']):print('REVIEW NEEDED',flush=True);break
print(read(),flush=True)
