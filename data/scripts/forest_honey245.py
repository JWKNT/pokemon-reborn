"""Complete one explicitly chosen Honey-tree obstacle through guarded UI steps."""
from play import *
mid,tree,bug=map(int,sys.argv[1:4]);label=sys.argv[4];foe=sys.argv[5]
assert foe in ['Pinsir','Heracross']
expected_opening={(283,108):367,(283,112):369,(283,110):368,(283,114):370,(283,115):371,(282,94):372,(282,96):373,(282,104):375,(289,60):339,(289,42):328}[(mid,bug)]
nav=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert not nav['switches'].get(str(expected_opening)), 'This forest obstacle is already open; no Honey spent'
if (mid,bug)==(283,114):assert nav['switches'].get('310'), 'Route1 log310 must open before this Pinsir can break log370'
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
if '--choice-open' not in sys.argv:run('eventq',mid,tree,'talk')
t=read().lower()
assert 'honey' in t and re.search(r'\b(?:yes|tes)\b',t),'Honey choice not visible'
act('c','wait:.8')
clear=0
for _ in range(12):
 r=snap();t=' '.join(z['text'] for z in r).lower();print(t,flush=True)
 if any(s in t for s in ['spread honey','flocked','across the tree']):act('c','wait:1');clear=0
 elif 'yes' in t or any(z['y']>.73 and len(z['text'])>18 for z in r):raise SystemExit('Honey dialogue review')
 else:
  clear+=1
  if clear>=3:break
  act('wait:.8')
else:raise SystemExit('Honey transition timeout')
run('checkpoint',label+'-Spawn')
encounter_epoch=time.time()
run('eventq',mid,bug,'talk')
t=read().lower();assert foe.lower() in re.sub(r'\s+','',t) and 'attacked' in re.sub(r'\s+','',t),'Expected forest encounter not visible'
act('c','wait:4')
run('battle_ready')
run('battle_batch','Zapdos',1,'--foes',foe,'--wild','--turns',6)
run('forest_tail245')
run('close_wild_music',foe,'--since',encounter_epoch)
run('checkpoint',label)

verified=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert verified['switches'].get(str(expected_opening)), f'Forest opening {expected_opening} did not activate; review prerequisites'
print('PERMANENT OPENING VERIFIED',expected_opening,flush=True)
