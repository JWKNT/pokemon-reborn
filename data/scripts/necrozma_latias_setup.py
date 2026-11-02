"""Finite first-Necrozma setup using only public HUD and ordinary controls."""
import json,re,subprocess,sys,time
from pathlib import Path
from play import ROOT,snap,NATIVE
from PIL import Image
journal=Path(sys.argv[1]);assert journal.resolve().is_relative_to(ROOT/'work') and not journal.exists()
stored_power='--stored-power' in sys.argv
data={'status':'running','calm_minds':0,'speed_item':False,'defense_item':False,'stored_power_plan':stored_power,'actions':[]}
def save():journal.write_text(json.dumps(data,indent=2)+'\n')
def state():
 rows=snap();text='\n'.join(r['text'] for r in rows);low=text.lower()
 assert all(w in low for w in ['fight','run']),('Command menu review',text)
 own=' '.join(r['text'] for r in rows if r['y']>.72 and r['x']<.5).lower()
 foe=' '.join(r['text'] for r in rows if r['y']<.37).lower()
 assert 'latias' in own and 'necrozma' in foe,('Public matchup changed',text)
 assert not re.search(r'\b(?:slp|par|frz)\b',low),('Status review',text)
 hp=[int(a) for a,b in re.findall(r'(\d+)\s*/+\s*(\d+)',text) if int(b)==508 and int(a)<=508]
 if len(hp)!=1:
  im=Image.open(NATIVE);w,h=im.size;p=ROOT/'work/necrozma-latias-own-hp.png'
  im.crop((int(w*.55),int(h*.40),int(w*.98),int(h*.70))).save(p)
  t=' '.join(r['text'] for r in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(p)])))
  hp=[int(a) for a,b in re.findall(r'(\d+)\s*/+\s*(\d+)',t) if int(b)==508 and int(a)<=508]
 assert len(hp)==1 and hp[0]>0,('Actual HP review',text)
 return {'epoch':time.time(),'hp':hp[0],'text':text}
try:
 for turn in range(20):
  before=state()
  if data['calm_minds']==6 and data['speed_item'] and (not stored_power or data['defense_item']) and before['hp']>=355:
   data['status']='completed';data['final']=before;save();print('LATIAS SETUP COMPLETE',before['hp'],flush=True);break
  if before['hp']<355:kind='recover';args=['battle_move.py','2','--watch']
  elif data['calm_minds']<6:
   kind='calm_mind';args=['battle_move.py','3','--watch']+(['--mega'] if data['calm_minds']==0 else [])
  elif not data['speed_item']:kind='x_speed';args=['battle_item.py','X Speed','Latias','--active']
  else:kind='x_defend';args=['battle_item.py','X Defend','Latias','--active']
  row={'kind':kind,'before':before,'pending':True};data['actions'].append(row);save()
  print('FINITE LATIAS SETUP',turn+1,kind,'HP',before['hp'],'CM',data['calm_minds'],flush=True)
  rc=subprocess.call([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]])
  row.update(returncode=rc,returned_epoch=time.time());save();assert rc==0,'Inspect partial action; never replay journal'
  after=state();row.update(pending=False,after=after)
  if kind=='calm_mind':data['calm_minds']+=1
  if kind=='x_speed':data['speed_item']=True
  if kind=='x_defend':data['defense_item']=True
  save()
 else:raise RuntimeError('Finite setup turn budget reached')
except Exception:
 data['status']='stopped_for_review';save();raise
