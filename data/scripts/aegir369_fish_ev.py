"""Normal fishing: Rayquaza EVs, with Arcanine Thief on Luvdisc for a Heart Scale.
Start at reviewed Tanzan Cove232[16,20], facing water, Rayquaza leading.
Never read live battle state. Owned EVs/items checked only after normal saves.
"""
from play import *
import difflib
from bgm_span import append_span,wild_track
start=int(sys.argv[1]);count=int(sys.argv[2]);assert 1<=count<=8

def run(s,*a):
 print('RAY TRAIN',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
foes=['Luvdisc','Basculin','Mantyke']
(ROOT/'notes/battle-control.json').write_text(json.dumps(dict(expected_foes=foes)))
wins=0
ray_move=2
if start>1:
 prior=json.loads((ROOT/'notes'/f'Aegir369-RayEV{start-1:02}-status.json').read_text())
 ray_prior=next(p for p in prior['party']if p['name']=='Rayquaza')
 if ray_prior['moves'][2]['pp']==0:ray_move=1
for cast in range(count*8):
 if wins>=count:break
 begin=time.time();run('fish_cast247')
 rows=snap();t=' '.join(r['text']for r in rows).lower()
 if 'fight' not in t:
  assert len(rows)<=4 and not re.search(r'\bhp\b',t),t
  continue
 enemy=' '.join(r['text'].lower()for r in rows if r['y']<.37)
 match=[n for n in foes if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in enemy.split())]
 assert len(match)==1,enemy
 foe=match[0]
 if foe=='Luvdisc':
  run('battle_switch','Arcanine');run('battle_batch','Arcanine',0,'--foes',foe,'--wild','--turns',3,'--min-hp','.6','--watch')
 else:run('battle_batch','Rayquaza',ray_move,'--foes',foe,'--wild','--turns',3,'--min-hp','.6','--watch')
 t=read().lower();assert len(t.splitlines())<=4 and not re.search(r'\bfight\b|\bhp\b|yes|no',t),t
 run('close_wild_music',foe,'--since',begin)
 wins+=1;label=f'Aegir369-RayEV{start+wins-1:02}'
 run('checkpoint',label)
 own=json.loads((ROOT/'notes'/f'{label}-status.json').read_text())
 ray=next(p for p in own['party']if p['name']=='Rayquaza')
 arca=next(p for p in own['party']if p['name']=='Arcanine')
 if ray['moves'][2]['pp']==0:ray_move=1
 assert ray['moves'][ray_move]['pp']>0, 'Rayquaza needs a normal PP restore'
 print('VERIFIED OWNED EV',ray['ev'],'ARCANINE HELD',arca['item'],flush=True)
 if arca['item']:
  assert arca['item']=='HEARTSCALE',arca['item']
  run('take_held','Arcanine','Heart Scale')
 if own['party'][0]['name']!='Rayquaza':run('party_front','Rayquaza')
else:raise SystemExit('Fishing cast bound reached')
print('EV BLOCK COMPLETE',wins,flush=True)
