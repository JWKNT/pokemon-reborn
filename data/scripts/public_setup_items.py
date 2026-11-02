"""Finite reviewed setup on one public matchup; never resumes/replays a pending item."""
import argparse,difflib,json,re,subprocess,sys,time
from pathlib import Path
from play import ROOT,read,snap
p=argparse.ArgumentParser();p.add_argument('actor');p.add_argument('max_hp',type=int);p.add_argument('foes');p.add_argument('items',type=json.loads);p.add_argument('journal',type=Path);p.add_argument('--min-hp',type=int,required=True);p.add_argument('--heal-item',default='Ultra Potion');p.add_argument('--heal-attempts',type=int,default=1);a=p.parse_args();assert 1<=a.heal_attempts<=6
assert 1<=len(a.items)<=6 and all(x in ['X Attack','X Defend','X Sp. Atk','X Sp. Def','X Accuracy','X Speed']for x in a.items)
assert not a.journal.exists() and 0<a.min_hp<=a.max_hp
data={'actor':a.actor,'max_hp':a.max_hp,'foes':a.foes.split(','),'items':a.items,'status':'running','events':[]};log=a.journal.with_suffix('.log')
def state():
 rows=snap();t='\n'.join(r['text']for r in rows);low=t.lower();assert 'fight' in low and any(r['text'].strip().lower() in ('bag','bae') for r in rows) and 'run' in low,('Public command required',t)
 own=' '.join(r['text']for r in rows if r['y']>.72 and r['x']<.5);norm=lambda z:re.sub('[^a-z]','',z.lower())
 assert norm(a.actor) in norm(own.replace('Mamile','Mawile').replace('Sylueon','Sylveon').replace('Sylweon','Sylveon').replace('Suampert','Swampert')),('Expected active actor',own)
 enemy=' '.join(r['text']for r in rows if r['y']<.37).replace('Meougtic','Meowstic').replace('Meoustic','Meowstic')
 assert any(difflib.SequenceMatcher(None,n.lower(),w.lower().strip('.,')).ratio()>=.8 for n in a.foes.split(',')for w in enemy.split()),('Matchup changed; stop',enemy)
 pairs=re.findall(r'(\d+)\s*/+\s*(\d+)',t);hp=[int(x)for x,y in pairs if int(y)==a.max_hp and int(x)<=a.max_hp]
 if len(hp)!=1:
  from PIL import Image
  from play import NATIVE
  im=Image.open(NATIVE);w,h=im.size;crop=ROOT/'work/setup-own-hp.png'
  im.crop((int(w*.55),int(h*.40),int(w*.98),int(h*.70))).save(crop)
  own_rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)]))
  own_text=' '.join(r['text']for r in own_rows)
  hp=[int(x)for x,y in re.findall(r'(\d+)\s*/+\s*(\d+)',own_text)if int(y)==a.max_hp and int(x)<=a.max_hp]
  t+='\nOWN HUD CROP: '+own_text
 assert len(hp)==1,('Unambiguous actual own HUD HP required',t)
 return {'epoch':time.time(),'hp':hp[0],'text':t}
def save():a.journal.write_text(json.dumps(data,indent=2)+'\n')
def use(item,out):
 before=state();e={'item':item,'before':before,'pending':True};data['events'].append(e);save();out.write('ITEM '+item+'\n');out.flush()
 r=subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),item,a.actor,*(['--active']if item.startswith('X ')else[])],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
 e.update(returncode=r.returncode,returned_epoch=time.time());save();assert r.returncode==0,'Inspect partial item; never replay'
 e.update(pending=False);save()
with log.open('x')as out:
 try:
  for item in a.items:
   observed=state()
   for attempt in range(a.heal_attempts):
    if observed['hp']>=a.min_hp:break
    use(a.heal_item,out);observed=state()
   assert state()['hp']>=a.min_hp,'Bounded healing did not establish action margin; inspect actual state'
   use(item,out);print('SETUP HELPER RETURN',item,flush=True)
  data['status']='completed';save();print('FINITE SETUP COMPLETE',flush=True)
 except Exception:
  data['status']='stopped_for_actual_state_review';save();raise
