"""Bounded low-level Thief farming; public UI only during each encounter.
Owned held items are checked only in normal saved checkpoints after battle.
"""
from play import *
import difflib
from bgm_span import append_span,wild_track
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 print('FARM',s,*a,flush=True)
 return subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
prefix=os.environ.get('REBORN_FARM_CHECKPOINT_PREFIX','Helix350')
assert re.fullmatch(r'[A-Za-z0-9-]+',prefix)
start_index=int(sys.argv[1]) if len(sys.argv)>1 else 1
control=ROOT/'notes/battle-control.json'
control.write_text(json.dumps({'expected_foes':['Luvdisc','Basculin','Mantyke']}))
wins=0;scales=0;target_scales=int(sys.argv[3]) if len(sys.argv)>3 else 2
for index in range(start_index,start_index+(int(sys.argv[2]) if len(sys.argv)>2 else 40)):
 if wins>=16 or scales>=target_scales:break
 begin=time.time()
 run('fish_cast247')
 rows=snap();t=' '.join(r['text']for r in rows).lower()
 if 'fight' not in t:
  assert len(rows)<=4 and not re.search(r'\bhp\b',t),t
  continue
 foes=['Luvdisc','Basculin','Mantyke']
 enemy=' '.join(r['text'].lower() for r in rows if r['y']<.37)
 matched=[n for n in foes if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in enemy.split())]
 assert len(matched)==1,enemy
 foe=matched[0]
 if foe!='Luvdisc':
  escaped=subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(begin)],env=E)
  if escaped.returncode==0:
   t=read().lower();assert len(t.splitlines())<=4 and not re.search(r'\bfight\b|\bhp\b',t),t
   print('FARM SKIPPED',index,foe,flush=True);continue
  t=read().lower()
  assert 'fight' in t and 'arcanine' in t, 'Failed escape needs review: '+t
  print('FARM ESCAPE FALLBACK: approved low-level KO',flush=True)
 run('battle_batch','Arcanine',0,'--foes',','.join(foes),'--wild','--turns',3,'--min-hp','.6','--watch')
 t=read().lower();assert len(t.splitlines())<=4 and not re.search(r'\bfight\b|\bhp\b',t),t
 run('close_wild_music',foe,'--since',begin)
 label=f'{prefix}-ScaleFish{index:02d}'
 assert not (ROOT/'backups'/f'Aster-{label}.rxdata').exists()
 run('checkpoint',label)
 own=json.loads((ROOT/'notes'/f'{label}-status.json').read_text())
 arcanine=next(p for p in own['party'] if p['name']=='Arcanine')
 assert arcanine['hp']>.6*arcanine['totalhp'],arcanine
 held=arcanine['item']
 if held:
  names={'HEARTSCALE':'Heart Scale','DEEPSEASCALE':'Deep Sea Scale','DEEPSEATOOTH':'Deep Sea Tooth'}
  assert held in names,held
  run('take_held','Arcanine',names[held])
  if held=='HEARTSCALE':scales+=1
 wins+=1
 print('FARM PROGRESS',index,'wins',wins,'scales',scales,flush=True)
run('checkpoint',f'{prefix}-ScaleFarmEnd{start_index}')
print('FARM FINISHED',wins,scales,flush=True)
