"""Execute clue/guide-derived ice slides; verify every normal movement endpoint."""
from play import *
from locate import locate
steps=json.loads((ROOT/'work/199-sapphire-ice-guide-plan.json').read_text())
start=int(sys.argv[1])if len(sys.argv)>1 else 0
for i,s in enumerate(steps):
 if i<start:continue
 assert locate(800)==(800,*s['start']),('Ice start mismatch',i)
 act(s['key']+':.18','wait:2')
 t=read();print(t,flush=True)
 if re.search(r'\bhp\b|\bfight\b',t,re.I):raise SystemExit('Battle interruption')
 actual=locate(800);assert actual==(800,*s['end']),(i,actual,s)
 print('ICE SLIDE VERIFIED',i,s,flush=True)
