"""Train Zeraora against the inspected Monday Jonah v4; normal UI only."""
from play import *
def run(name,*args):
 p=subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 print(p.stdout,flush=True)
 if p.returncode:raise SystemExit('Helper stopped: '+name)
 return p.stdout
for cycle in range(int(sys.argv[1])):
 if not (cycle==0 and '--dialog-open' in sys.argv):run('eventq',38,41,'talk')
 run('trainer_music','start','YOUNGSTER','Jonah','--map',38)
 run('choose_dialog','Yes|No','Yes')
 run('trainer_enter',38,41,'YOUNGSTER','Jonah','--expand-common','--active-dialogue','--past-choice','--resume-intro')
 out=run('battle_batch','Zeraora',1,'--foes','Squirtle,Wartortle,Blastoise','--turns',12,'--stay-team-reviewed','--min-hp',.4,'--watch','--stop-after-battle')
 assert re.search(r'de.?feated|for winning',out,re.I),'Victory not observed'
 out+=run('dialog','--limit=20')
 assert 'bonus' in out.lower() or 'cand' in out.lower(),'Reward not observed'
 run('trainer_music','finish')
 print('JONAH TRAINING COMPLETE',cycle+1,flush=True)
