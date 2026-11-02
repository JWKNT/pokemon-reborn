"""Small reviewed preparation phases via normal controls; each stops on guards."""
import json,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
def run(s,*args):
 print('STAGE',s,*args,flush=True)
 env=dict(os.environ)
 if s in ['eventq','q']:env['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True,cwd=ROOT,env=env)
phase=sys.argv[1]
if phase=='berries':
 run('checkpoint','Saphira-Swamp-before-berries')
 st=json.loads((ROOT/'notes/Saphira-Swamp-before-berries-status.json').read_text())
 mon=next(m for m in st['party'] if m['species']=='SWAMPERT')
 assert mon['ev']==[32,155,59,159,32,73],mon['ev']
 assert st['trainer']['money']>=8500
 run('eventq',355,136,'talk');run('mart_open')
 for item,count in [('Qualot Berry',3),('Hondew Berry',8),('Grepa Berry',2),('Tamato Berry',4)]:run('shop_buy',item,count,500)
 run('mart_exit')
 for item,count in [('Qualot Berry',3),('Hondew Berry',8),('Grepa Berry',2),('Tamato Berry',4)]:run('berry_batch',item,'Swampert',count)
 run('checkpoint','Saphira-Swamp-berries-used')
 st=json.loads((ROOT/'notes/Saphira-Swamp-berries-used-status.json').read_text())
 mon=next(m for m in st['party'] if m['species']=='SWAMPERT')
 assert mon['ev']==[32,155,0,0,0,0],mon['ev']
elif phase=='arcanine-berries':
 run('checkpoint','Saphira-Arcanine-before-berries')
 st=json.loads((ROOT/'notes/Saphira-Arcanine-before-berries-status.json').read_text())
 mon=next(m for m in st['party'] if m['species']=='ARCANINE')
 assert mon['ev']==[34,114,121,107,44,90],mon['ev']
 assert st['trainer']['money']>=10500
 if '--purchased' not in sys.argv:
  run('eventq',355,136,'talk');run('mart_open')
  for item,count in [('Kelpsy Berry',6),('Qualot Berry',7),('Grepa Berry',3),('Tamato Berry',5)]:run('shop_buy',item,count,500)
  run('mart_exit')
 else:
  assert all(st['bag']['contents'][k]>=n for k,n in [('KELPSYBERRY',6),('QUALOTBERRY',7),('GREPABERRY',3),('TAMATOBERRY',5)])
 for item,count in [('Kelpsy Berry',6),('Qualot Berry',7),('Grepa Berry',3),('Tamato Berry',5)]:run('berry_batch',item,'Arcanine',count)
 run('checkpoint','Saphira-Arcanine-berries-used')
 st=json.loads((ROOT/'notes/Saphira-Arcanine-berries-used-status.json').read_text())
 mon=next(m for m in st['party'] if m['species']=='ARCANINE')
 assert mon['ev']==[34,0,0,107,0,0],mon['ev']
elif phase=='curse':
 from play import read,act
 run('eventq',355,35,'talk')
 run('choose_dialog','Teach one-by-one.|Remember all.|No','Teach one-by-one.','--source',355,35)
 for _ in range(5):
  t=read().lower()
  if 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):break
  assert 'which pok' in t or 'klhich pok' in t,t
  act('c','wait:.5')
 else:raise SystemExit('Reminder party entry timeout')
 run('party_pick','Cofagrigus','--single')
 for _ in range(5):
  t=read().lower()
  if 'teach which' in t:break
  assert "what'll it be" in t or 'whatll it be' in t,t
  act('c','wait:.5')
 else:raise SystemExit('Reminder list timeout')
 run('relearn_select','Curse',7,3)
 run('overworld');run('checkpoint','Saphira-Cofagrigus-Curse')
elif phase=='ice-punch':
 from play import read,act
 if '--at-payment' not in sys.argv:
  run('eventq',355,129,'talk')
  run('choose_dialog','Dual Chop|Thunder Punch|Fire Punch|Ice Punch','Ice Punch')
 run('choose_dialog','Yes|No','Yes')
 for _ in range(5):
  t=read().lower()
  if 'cancel' in t and (t.count('hp')>=5 or 'teach which' in t):break
  assert 'which pok' in t or 'choose a pok' in t,t
  act('c','wait:.5')
 else:raise SystemExit('Tutor party entry timeout')
 run('party_pick','Swampert','--single')
 from learning import PLANS,resolve
 PLANS['ice punch']=2
 t=read()
 assert 'icepunch' in ''.join(t.lower().split()) and 'swampert' in t.lower(),t
 assert resolve(t),'Tutor learning prompt requires review'
 # Tutor returns to its four-move menu; do not blindly confirm another purchase.
 from play import snap
 for _ in range(15):
  t=read().lower()
  if all(z in t for z in ['dual chop','fire punch','ice punch']):
   act('x','wait:.7');break
  assert any(z in t for z in ['learned','and','poof','forgot','settle things']),t
  act('c','wait:.6')
 else:raise SystemExit('Tutor completion review')
 run('dialog','--limit=12')
 run('overworld');run('checkpoint','Saphira-Swampert-IcePunch')
else:raise SystemExit('Unknown phase')
