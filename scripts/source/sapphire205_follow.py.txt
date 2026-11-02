"""Bounded normal-control execution of a static Sapphire proposal; stop on mismatch."""
from play import *
from locate import locate
proposal=pathlib.Path(sys.argv[sys.argv.index('--plan')+1]) if '--plan' in sys.argv else ROOT/'work/205-sapphire-proposal.json'
steps=json.loads(proposal.read_text())['steps']
a=int(sys.argv[1]);end=int(sys.argv[2]);assert 0<=a<end<=len(steps)
os.environ.setdefault('REBORN_COORD_CACHE','1')
journal=ROOT/'work/sapphire205-progress.jsonl'
def run(script,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*map(str,args)],check=True)
def world():
 rr=snap();text=' '.join(v['text']for v in rr).lower()
 if re.search(r'\bhp\b|\bfight\b|\bwild\b|pp:',text):raise SystemExit('Unexpected battle; stop Sapphire follower')
 if 'repel' in text and ('wore' in text or 'uore' in text):run('renew_repel');return 'repel'
 if any(v['y']>.72 and len(v['text'])>10 for v in rr):run('dialog','--yes','--limit=10')
position=locate(804)
while a<end:
 s=steps[a];first=a
 expected=tuple(s.get('start',s.get('stand')));assert position==(804,*expected),('Sapphire starting position',a,expected)
 print('SAPPHIRE STEP',a,s,flush=True)
 if s['kind']=='crystal':
  nav=json.loads((ROOT/'notes/navigation-state.json').read_text());assert not nav['switches'].get(str(s['switch']),False)
  act(s['key']+':.18','c','wait:1');text=read();assert 'reacted to the crystal' in text.lower(),text
  run('dialog','--limit=12');run('checkpoint',f'Sapphire-Crystal-{s["eid"]}')
  nav=json.loads((ROOT/'notes/navigation-state.json').read_text());assert nav['switches'][str(s['switch'])] is True
  position=(804,*json.loads((ROOT/'notes'/f'Sapphire-Crystal-{s["eid"]}-status.json').read_text())['position'])
 elif s['kind']=='climb':
  act(s['key']+':.18','c','wait:1');world();position=locate(804);assert position==(804,*s['end']),('Sapphire climb landing',a,s)
 elif s['kind']=='slide':
  act(s['key']+':.12','wait:2');world();position=locate(804);assert position==(804,*s['end']),('Sapphire slide endpoint',a,s)
 else:
  batch=[]
  while a<end and steps[a]['kind']=='walk' and len(batch)<24:
   batch.append(steps[a]);a+=1
  a-=1;assert all(x['end']==y['start']for x,y in zip(batch,batch[1:]))
  act(*[x['key']+':.12'for x in batch])
  interruption=world();position=locate(804)
  if position!=(804,*batch[-1]['end']):
   matches=[first+i for i,x in enumerate(batch) if position==(804,*x['start'])]
   assert interruption=='repel' and len(matches)==1,('Sapphire walk endpoint',first,a,position,batch[-1])
   a=matches[0];print('RESUME AFTER OBSERVED REPEL',a,position,flush=True);continue
 with journal.open('a')as f:f.write(json.dumps(dict(proposal=str(proposal),first=first,last=a,epoch=time.time(),status='normal movement endpoint verified'))+'\n')
 a+=1
run('checkpoint',f'Sapphire-Queue-{end}')
