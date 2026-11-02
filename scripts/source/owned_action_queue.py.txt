"""Finite root-reviewed normal actions with numeric OWN Q HP guards.

No automatic resume, switches, opponent inspection, battle-log or runtime read.
Dry-run reads only the explicit frozen own checkpoint and plan. Execute binds
one recording process, one UI owner and a new journal before any input.
"""
import argparse,difflib,json,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
norm=lambda s:re.sub('[^a-z]','',s.lower()).replace('suampert','swampert').replace('sylueon','sylveon').replace('sylweon','sylveon').replace('sulueon','sylveon').replace('sulveon','sylveon').replace('manaswine','mamoswine').replace('mamaswine','mamoswine').replace('roton','rotom')
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('roster',type=Path);p.add_argument('plan',type=Path)
 p.add_argument('journal',type=Path);p.add_argument('--execute',action='store_true');p.add_argument('--hud-only',action='store_true',help='Single battle HP guards from public own HUD; field guards still use owned Q');a=p.parse_args()
 names={m['name']:m for m in json.loads(a.roster.read_text())['party']}
 plan=json.loads(a.plan.read_text());assert 1<=len(plan)<=12
 for s in plan:
  assert set(s)<={'actor','foes','min_hp','item','move_slot','target','heal_item','field','double'}
  assert type(s.get('double',True)) is bool
  assert s['actor'] in names and 0<s['min_hp']<=names[s['actor']]['totalhp']
  assert 1<=len(s['foes'])<=16 and all(type(n)is str and n for n in s['foes'])
  assert ('item' in s)^('move_slot' in s)
  if 'move_slot' in s:assert s['move_slot'] in range(4) and s.get('target') in [None,1,3]
  else:assert s['item'] in ['X Attack','X Defend','X Sp. Atk','X Sp. Def','X Speed','X Accuracy','Ultra Potion','Max Potion','Full Heal','Lemonade'] and 'target' not in s
  assert s.get('heal_item','Ultra Potion') in ['Ultra Potion','Max Potion','Lemonade']
 if not a.execute:print(json.dumps(plan,indent=2));return
 from play import snap
 assert not a.journal.exists()
 health=ROOT/'recordings/capture-health.json';baseline=json.loads(health.read_text())
 data={'roster':str(a.roster.resolve()),'plan':plan,'status':'running','events':[]};heals=0
 def save():a.journal.write_text(json.dumps(data,indent=2)+'\n')
 def call(helper,*args):
  subprocess.run([sys.executable,str(ROOT/'scripts'/(helper+'.py')),*map(str,args)],check=True)
 def state(s,i,phase):
  h=json.loads(health.read_text());assert h['active'] and time.time()-h['epoch']<8
  assert h['pid']==baseline['pid'] and h['restart_count']==baseline['restart_count']
  rows=snap();text=' '.join(r['text'] for r in rows)
  assert 'fight' in text.lower() and re.search(r'\b(?:bag|bae)\b',text,re.I),text
  prompt=' '.join(r['text'] for r in rows if r['y']>.72 and r['x']<.55)
  assert norm(s['actor']) in norm(prompt),('Owned command changed',prompt)
  observed=[]
  for lo,hi in ([(.08,.21),(.21,.37)] if s.get('double',True) else [(.08,.37)]):
   band=[r for r in rows if r['x']<.5 and lo<r['y']<hi]
   hits={n for n in s['foes'] for r in band if difflib.SequenceMatcher(None,norm(n),norm(r['text'])).ratio()>.82}
   hud=any(re.search(r'\bhp\b|l[uv].?\s*\d+',r['text'],re.I) for r in band)
   assert (len(hits)==1 if hud else len(hits)<=1),('Expected public opponent band needs review',band)
   observed.extend(hits)
  assert 1<=len(set(observed))<=2,('Expected public opponents not readable',text)
  proof=a.journal.with_name(a.journal.stem+f'-step{i:02}-{phase}.json')
  if a.hud_only and not s.get('double',True) and not s.get('field'):
   proof.write_text(json.dumps({'actor':s['actor'],'source':'Fresh public single battle own HP HUD','observations':rows},indent=2)+'\n')
   body=text
  else:
   call('own_field_inspect',s['actor'],proof)
   own=json.loads(proof.read_text());body='\n'.join(o['text'] for o in own['observations'])
  if s.get('field'):assert 'fieldeffect'+norm(s['field']) in norm(body),('Field changed',body)
  # Single-battle owned Q omits HP; the numeric OWN command HUD displays it.
  hp_body=body if s.get('double',True) else '\n'.join(r['text'] for r in rows if r['x']>.5 and .40<r['y']<.71)
  hp=[int(x) for x,y in re.findall(r'(\d+)\s*,?\s*/+\s*(\d+)',hp_body) if int(y)==names[s['actor']]['totalhp'] and 0<int(x)<=names[s['actor']]['totalhp']]
  if not s.get('double',True):
   for _ in range(4):
    if len(hp)==1:break
    retry=snap()
    assert 'fight' in ' '.join(r['text']for r in retry).lower(), 'Command changed during read-only HP retry'
    hp_body='\n'.join(r['text']for r in retry if r['x']>.5 and .40<r['y']<.71)
    hp=[int(x) for x,y in re.findall(r'(\d+)\s*,?\s*/+\s*(\d+)',hp_body) if int(y)==names[s['actor']]['totalhp'] and 0<int(x)<=names[s['actor']]['totalhp']]
  assert len(hp)==1,('Own numeric HP required',body,hp_body)
  return {'epoch':time.time(),'hp':hp[0],'foes':observed,'proof':str(proof)}
 try:
  save()
  for i,s in enumerate(plan):
   before=state(s,i,'before');event={'index':i,'before':before,'pending':False};data['events'].append(event);save()
   if before['hp']<s['min_hp']:
    assert heals<3,'Healing budget exhausted; inspect actual state'
    event['pending']=s.get('heal_item','Ultra Potion');save();call('battle_item',event['pending'],s['actor']);heals+=1
    event['pending']=False;event['after_heal']=state(s,i,'after-heal');save()
    assert event['after_heal']['hp']>=s['min_hp'],'One heal did not establish margin; inspect rather than loop'
   event['pending']={'kind':'item' if 'item' in s else 'move','value':s.get('item',s.get('move_slot'))};save()
   if 'item' in s:call('battle_item',s['item'],s['actor'],*(['--active'] if s['item'].startswith('X ') else []))
   else:call('battle_move',s['move_slot'],*([s['target']] if s.get('target') is not None else []),'--watch')
   event.update(pending=False,returned_epoch=time.time());save()
   if 'move_slot' in s:call('battle_ready')
   print('GUARDED ACTION RETURN',i,flush=True)
  final_plan={k:v for k,v in plan[-1].items() if k!='field'}
  data['final_state']=state(final_plan,len(plan),'final');data['status']='completed';save()
 except Exception:
  data['status']='stopped_for_actual_state_review';save();raise
if __name__=='__main__':main()
