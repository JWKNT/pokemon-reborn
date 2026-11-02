"""Execute a reviewed Regigigas boulder plan through normal controls; save every straight group."""
import json,pathlib,subprocess,sys,itertools
R=pathlib.Path(__file__).resolve().parents[1];plan=json.loads(pathlib.Path(sys.argv[1]).read_text());eid=int(sys.argv[2]);assert plan['map']==840 and eid in [79,80]
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['variables']['588']==13
current=s['positions']['840'][str(eid)];pushes=plan['pushes'];assert all(p['event']==eid for p in pushes)
if current!=plan['initial'][str(eid)]:
 matches=[i for i,p in enumerate(pushes)if p['box_to']==current];assert len(matches)==1;pushes=pushes[matches[0]+1:]
session=json.loads((R/'notes/current-run-control.json').read_text())['session']
for i,(direction,items)in enumerate(itertools.groupby(pushes,lambda p:p['direction'])):
 group=list(items);assert 1<=len(group)<=20
 run('q','840,'+','.join(map(str,group[0]['from'])))
 seq=[]
 for j in range(len(group)):
  seq += [direction+':.12','wait:.65']
  if j<len(group)-1:seq += [direction+':.12','wait:.25']
 run('play',*seq)
 run('checkpoint',f'Postgame{session}-Boulder{eid}-{i}')
 s=json.loads((R/'notes/navigation-state.json').read_text());assert s['positions']['840'][str(eid)]==group[-1]['box_to'],(s['positions']['840'][str(eid)],group[-1])
 print('SAVED BOULDER GROUP',eid,group[-1]['box_to'],flush=True)
