"""Train owned Latias while gathering Heart Scales with ordinary Thief encounters."""
from play import *
import difflib
from public_owned_hp import read as read_hp

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
phase=sys.argv[1];assert phase in ['hp','def'];arc_total=int(sys.argv[2]);assert 300<=arc_total<=600
# Caller starts at the inspected fishing shore, Latias first, Arcanine itemless,
# holding Power Weight or Power Belt on Latias; low-level native Good Rod pool.
wins=int(sys.argv[3])if len(sys.argv)>3 else 0;assert 0<=wins<8
foes=['Luvdisc','Basculin','Mantyke']
cpath=ROOT/'notes/battle-control.json';control=json.loads(cpath.read_text());control.update(stop=False,expected_foes=foes);cpath.write_text(json.dumps(control,indent=2))
for cast in range(1,51):
 if wins>=8:break
 began=time.time();run('fish_cast247');rows=snap();t=' '.join(r['text']for r in rows).lower()
 if 'fight' not in t:
  assert len(rows)<=4 and not re.search(r'\bhp\b',t),t
  continue
 enemy=' '.join(r['text'].lower()for r in rows if r['y']<.37)
 found=[n for n in foes if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in enemy.split())]
 assert len(found)==1,enemy
 assert 'latias' in t,'Lead requires review: '+t
 if found[0]=='Luvdisc':
  run('battle_switch','Arcanine');run('battle_ready')
  rows=snap();hp=read_hp(rows,arc_total)
  if hp < .75*arc_total:
   run('battle_move',3,'--watch');run('battle_ready')
  run('battle_batch','Arcanine',0,'--foes',','.join(foes),'--wild','--turns',3,'--min-hp','.6','--watch')
 else:
  run('battle_batch','Latias',1,'--foes',','.join(foes),'--wild','--turns',3,'--min-hp','.6','--watch')
 t=read().lower();assert len(t.splitlines())<=4 and not re.search(r'\bfight\b|\bhp\b',t),t
 run('close_wild_music',found[0],'--since',began)
 wins+=1;label=f'Idyll320-Latias-{phase}{wins}'
 assert not (ROOT/f'backups/Aster-{label}.rxdata').exists()
 run('checkpoint',label);j=json.loads((ROOT/f'notes/{label}-status.json').read_text())
 lat=next(m for m in j['party']if m['species']=='LATIAS');arc=next(m for m in j['party']if m['species']=='ARCANINE')
 expected=[min(252,wins*32),0,0,0,0,0]if phase=='hp'else[252,0,min(252,wins*32),0,0,0]
 assert lat['ev']==expected,(lat['ev'],expected)
 assert lat['hp']>.6*lat['totalhp'] and arc['hp']>.6*arc['totalhp'],'Health review'
 held=arc['item']
 if held:
  names={'HEARTSCALE':'Heart Scale','DEEPSEASCALE':'Deep Sea Scale','DEEPSEATOOTH':'Deep Sea Tooth'}
  assert held in names,held
  run('take_held','Arcanine',names[held])
 print('VERIFIED LATIAS EV',phase,wins,expected,'loot',held,flush=True)
assert wins==8,'Fishing cast limit; resume from verified progress'
run('checkpoint',f'Idyll320-Latias-{phase}Complete')
