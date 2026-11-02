"""Normal Kricketune preparation; bounded UI phases, frozen-state verification."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*args):
 env=dict(os.environ,REBORN_COORD_CACHE='1')
 if s!='fly_to':env['REBORN_FAST_KEYS']='1'
 else:env.pop('REBORN_FAST_KEYS',None)
 print('STAGE',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],check=True,env=env)
def check(label,ev=None):
 run('checkpoint',label)
 s=json.loads((R/'notes'/f'{label}-status.json').read_text());m=next(m for m in s['party'] if m['species']=='KRICKETUNE')
 if ev is not None:assert m['ev']==ev,(m['ev'],ev)
 return m
phase=sys.argv[1]
if phase in ['hp','speed']:
 p=R/'notes/battle-control.json';c=json.loads(p.read_text());c.update(stop=False,expected_foes=['Noibat','Woobat']);p.write_text(json.dumps(c))
if phase=='berries':
 run('eventq',355,136,'talk');run('mart_open')
 for item,n in [('Kelpsy Berry',2),('Qualot Berry',2),('Hondew Berry',3),('Grepa Berry',1)]:run('shop_buy',item,n,500)
 run('mart_exit')
 for item,n in [('Kelpsy Berry',2),('Qualot Berry',2),('Hondew Berry',3),('Grepa Berry',1)]:run('berry_batch',item,'Kricketune',n)
 check('Krik217-Berries',[16,0,0,0,0,51])
elif phase in ['railnet','railnet-resume-held']:
 if phase=='railnet':run('give_held','Power Weight','Kricketune','--single-step')
 run('party_front','Kricketune')
 run('eventq',355,118,'talk');run('heal');run('fly_to',519)
 run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
 check('Krik217-Railnet',[16,0,0,0,0,51])
elif phase=='hp':
 run('train_wild_bulk','Kricketune',0,8,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger')
 check('Krik217-HP',[252,0,0,0,0,51])
elif phase=='speed':
 run('give_held','Power Anklet','Kricketune','--single-step')
 run('train_wild_bulk','Kricketune',0,7,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger')
 check('Krik217-EV',[252,0,0,0,0,252])
 run('take_held','Kricketune','Power Anklet')
else:raise SystemExit('Unknown phase')
