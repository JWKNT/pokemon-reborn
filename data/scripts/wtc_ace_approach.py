"""Open the office, heal, refuse Taka, and enter the reviewed Ace encounter."""
from play import *
from locate import locate

stage=int(sys.argv[1])if len(sys.argv)>1 else 1
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
if stage<=1:
 s=json.loads((ROOT/'notes/navigation-state.json').read_text())
 assert s['variables'].get('276')==24
 assert all(s['variables'].get(str(i))==3 for i in range(256,265))
 assert locate(505)[0]==505
 run('surface_walk',505,24,11)
 run('wtc_gate',505,38)
 run('touch_heal',505,18,'--surface')
 run('party_lead','Arcanine')
 run('checkpoint','WTC-Ace-ready')
 print('ACE PREPARATION COMPLETE',flush=True)
if stage<=2:
 run('surface_event',505,20,'enter')
 run('linear_dialog',478,10,'--until-choice','--past-battle','--burst','--log-scripted-bgm')
 run('choose_dialog','Yes|No','No')
 print('TAKA BATTLE REFUSED THROUGH NORMAL CHOICE',flush=True)
if stage<=3:
 run('trainer_enter',478,10,'ACESPADES','Ace of Spades','--active-dialogue','--past-choice')
