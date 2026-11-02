"""Normal preparation routes and bounded reward-verified Indra rounds."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1')
 if s in ['eventq','q']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
def saved(label):return json.loads((R/'notes'/f'{label}-status.json').read_text())
phase=sys.argv[1]
if phase=='circus':
 x=saved('Gyarados181-level45');g=next(m for m in x['party']if m['species']=='GYARADOS')
 assert g['level']==45 and [m['move']for m in g['moves']]==['SPLASH','TACKLE','CRUNCH','DRAGONDANCE']
 run('give_held','Charcoal','Arcanine')
 run('eventq',38,6,'enter');run('fly_to',355,'--carrier','Tranquill')
 run('eventq',355,83,'talk');run('mart_open');run('shop_buy','Power Anklet',1,15000);run('mart_exit')
 run('eventq',355,118,'talk');run('heal');run('checkpoint','Gyarados181-Circus-ready')
elif phase=='indra':
 start,count=map(int,sys.argv[2:4]);assert 1<=start<=7 and 1<=count<=3 and start+count<=8
 for i in range(start,start+count):
  before=saved('Gyarados181-Circus-ready' if i==1 else f'Gyarados181-Indra-{i-1}')['bag']['contents'].get('EXPCANDYXL',0)
  run('saphira_indra_candy','--turbo','--plan',R/'work/session181-indra-plan.json')
  run('eventq',355,118,'talk');run('heal');label=f'Gyarados181-Indra-{i}';run('checkpoint',label)
  after=saved(label)['bag']['contents'].get('EXPCANDYXL',0)
  assert after==before+5,(before,after)
  print('NORMAL CANDY REWARD VERIFIED',i,after,flush=True)
elif phase=='level95':
 label='Gyarados181-Indra-7';x=saved(label)
 g=next(m for m in x['party']if m['species']=='GYARADOS');assert g['level']==45
 code="v=load_rgss(ARGV[0]);p=v[:Trainer].instance_variable_get(:@party);g=p.find{|m|m.instance_variable_get(:@species)==:GYARADOS};puts g.instance_variable_get(:@exp)"
 exp=int(subprocess.check_output(['ruby','-r',str(R/'scripts/read_rgss.rb'),'-e',code,str(R/'backups'/f'Aster-{label}.rxdata')],stderr=subprocess.DEVNULL))
 count=((5*95**3)//4-exp+29999)//30000
 assert 1<=count<=x['bag']['contents']['EXPCANDYXL']
 print('FROZEN EXPERIENCE / REQUIRED XL',exp,count,flush=True)
 run('train_candy_one','Gyarados',count,'XL');run('checkpoint','Gyarados181-level95')
 g=next(m for m in saved('Gyarados181-level95')['party']if m['species']=='GYARADOS')
 assert g['level']==95 and g['ev']==[0]*6
elif phase in ('ev','ev-after-waterfall','ev-on-strip'):
 if phase=='ev-after-waterfall':
  ready=next(m for m in saved('Gyarados182-Waterfall-ready')['party']if m['species']=='GYARADOS')
  assert ready['moves'][0]['move']=='WATERFALL' and ready['ev']==[0]*6
 g=next(m for m in saved('Gyarados181-level95')['party']if m['species']=='GYARADOS')
 assert g['level']==95 and g['ev']==[0]*6
 if phase=='ev-on-strip':
  ready=saved('Gyarados181-EV-ready');lead=ready['party'][0]
  assert ready['map']==633 and lead['species']=='GYARADOS' and lead['item']=='POWERBRACER' and lead['ev']==[0]*6
 if phase!='ev-on-strip':
  if phase=='ev':run('teach_machine','TMX5','Gyarados','Waterfall',0,'--single-step',*(['--bag-open'] if '--bag-open' in sys.argv else []))
  run('give_held','Power Bracer','Gyarados');run('party_front','Gyarados')
  run('fly_to',519,'--carrier','Tranquill')
  run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,14,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
  run('checkpoint','Gyarados181-EV-ready')
 run('train_wild_bulk','Gyarados',2,8,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal')
 run('checkpoint','Gyarados181-Attack-trained')
 g=next(m for m in saved('Gyarados181-Attack-trained')['party']if m['species']=='GYARADOS');assert g['ev']==[0,252,0,0,0,0]
 run('give_held','Power Anklet','Gyarados')
 run('train_wild_bulk','Gyarados',0,8,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--dense-horizontal')
 run('checkpoint','Gyarados181-EV-trained')
 g=next(m for m in saved('Gyarados181-EV-trained')['party']if m['species']=='GYARADOS');assert g['ev']==[0,252,0,0,0,252]
 run('take_held','Gyarados','Power Anklet');run('field_repel','Super Repel');run('eventq',633,3,'enter')
 run('fly_to',530,'--carrier','Tranquill');run('eventq',530,11,'enter')
 run('checkpoint','Gyarados181-Outrage-ready')
else:raise SystemExit('Unknown phase')
