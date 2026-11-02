"""Continue reviewed Luna setup after one manually verified XDefend. Ordinary UI only."""
from play import *
from luna_arcanine_setup import Queue,named,level_seen,hp_pair
from types import SimpleNamespace
from PIL import Image
args=SimpleNamespace(prior_journal=None,canvas=(112,132,2048,1536),journal=ROOT/'notes/luna-manual-setup-1.json')
assert not args.journal.exists(),'Do not replay this setup'
q=Queue.__new__(Queue);q.Image=Image;q.canvas=args.canvas;q.journal_path=args.journal;q.journal={'created_epoch':time.time(),'policy':'Guarded ordinary UI queue with final native bag reconciliation'};q.templates=q.status_templates();stages={'Defense':2,'Speed':0,'Sp.Def':0,'Sp.Atk':0};actions=[{'item':'X Defend','evidence':'Root observed 264/294 first command; prior item helper exit0; first self item.','manual':True}]
def guard():
 for _ in range(3):
  rows=snap();text='\n'.join(x['text']for x in rows)
  prompt=' '.join(x['text']for x in rows if x['y']>.72 and x['x']<.55)
  foe=' '.join(x['text']for x in rows if x['y']<.37 and x['x']<.5)
  if 'FIGHT' not in text or not named(prompt,'arcanine') or not named(foe,'weavile') or not level_seen(foe,83):time.sleep(.2);continue
  hp,total=hp_pair(text,294);status,error,dy=q.status(Image.open(NATIVE).convert('RGB'))
  frac=q.hp_bar(Image.open(NATIVE).convert('RGB'),dy)
  assert abs(frac-hp/total)<.05,'Visible HP disagreement'
  assert status in ['none','poison'],'Unexpected status'
  return hp,status,text
 raise SystemExit('Actor/foe/level command needs review')
def use(item,hp,status):
 rec={'item':item,'start':time.time(),'hp_before':hp,'status_before':status};actions.append(rec);q.journal.update(actions=actions,stages=stages,pending=rec);q.write()
 cmd=[sys.executable,str(ROOT/'scripts/battle_item.py'),item,'Arcanine']
 if item.startswith('X '):cmd+=['--active']
 subprocess.run(cmd,check=True);subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
 hp,status,text=guard();rec.update(end=time.time(),hp_after=hp,status_after=status,ui=text);q.journal.update(pending=None);q.write();print(item,'resolved',hp,status,flush=True)
 return hp,status
for item in ['X Speed','X Defend','X Sp.Def','X Sp.Def','X Sp.Atk','X Sp.Atk','X Sp.Atk']:
 hp,status,text=guard()
 for _ in range(8):
  if hp>=180 and status=='none':break
  hp,status=use('Ultra Potion'if hp<180 else'Full Heal',hp,status)
 else:raise SystemExit('Heal/cure budget review')
 hp,status=use(item,hp,status);stat={'X Speed':'Speed','X Defend':'Defense','X Sp.Def':'Sp.Def','X Sp.Atk':'Sp.Atk'}[item];stages[stat]+=2;q.journal['stages']=stages;q.write()
q.journal.update(complete=True,pending=None,finished_epoch=time.time());q.write();print('REMAINING LUNA SETUP COMPLETE',hp,status,stages,flush=True)
