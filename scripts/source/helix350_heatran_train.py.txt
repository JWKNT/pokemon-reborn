"""Bounded normal Good Rod training of owned Heatran; verify EVs after fights."""
from play import *
import difflib
phase=sys.argv[1];assert phase in ('hp','spa')
wins=int(sys.argv[2]) if len(sys.argv)>2 else 0
assert 0<=wins<8
foes=['Luvdisc','Basculin','Mantyke']
(ROOT/'notes/battle-control.json').write_text(json.dumps({'expected_foes':foes}))
def run(s,*args):
 print('TRAIN',s,*args,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,args)],check=True)
for cast in range(50):
 if wins>=8:break
 began=time.time();run('fish_cast247');rows=snap();t=' '.join(r['text'] for r in rows).lower()
 if 'fight' not in t:
  assert len(rows)<=4 and not re.search(r'\bhp\b',t),t
  continue
 enemy=' '.join(r['text'].lower() for r in rows if r['y']<.37)
 found=[n for n in foes if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in enemy.split())]
 assert len(found)==1 and 'heatran' in t,t
 run('battle_batch','Heatran',1 if phase=='hp' else 2,'--foes',','.join(foes),'--wild','--turns',3,'--min-hp','.6','--watch')
 t=read().lower();assert len(t.splitlines())<=4 and not re.search(r'\bfight\b|\bhp\b',t),t
 run('close_wild_music',found[0],'--since',began)
 wins+=1;label=f'Helix350-Heatran-{phase}{wins}'
 assert not (ROOT/'backups'/f'Aster-{label}.rxdata').exists()
 run('checkpoint',label)
 s=json.loads((ROOT/'notes'/f'{label}-status.json').read_text())
 p=next(x for x in s['party'] if x['species']=='HEATRAN')
 expected=[min(252,32*wins),0,0,0,0,0] if phase=='hp' else [252,0,0,min(252,32*wins),0,0]
 assert p['ev']==expected,(p['ev'],expected)
 assert p['hp']>.6*p['totalhp'],p
 print('HEATRAN EV VERIFIED',phase,wins,expected,flush=True)
assert wins==8,'Cast limit; resume from verified checkpoint'
