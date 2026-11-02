from play import *
from nav import loadmap
x=int(sys.argv[1]);answer=sys.argv[2]
r=subprocess.run([sys.executable,str(ROOT/'scripts/go.py'),str(x),'4'])
if r.returncode:raise SystemExit(r.returncode)
act('up','c','wait:0.8');txt=read();print(txt,flush=True)
if 'true' not in answer.lower():
 act('c','wait:0.5')
 seq=[]
 for i,n in enumerate(str(int(answer)).zfill(3)[::-1]):
  if i:seq.append('left')
  n=int(n);seq += ['up']*n if n<=5 else ['down']*(10-n)
 act(*seq,'c','wait:0.8')
else:act('c','wait:0.8')
txt=read();print(txt,flush=True)
if answer.lower()=='true' and 'true' in txt.lower() and ('false' in txt.lower() or 'falze' in txt.lower()):
 act('c','wait:0.8');txt=read();print(txt,flush=True)
if 'correct' not in txt.lower() or 'incorrect' in txt.lower():raise SystemExit('Quiz result needs review')
act('c','wait:0.5');print(read(),flush=True)
