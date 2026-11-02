"""Reviewed normal-control recovery, storage, training and HM preparation."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--resume-pc' not in sys.argv:
 run('eventq',702,6,'talk')
 run('linear_dialog',702,6,'--active','--until-choice')
 run('choose_dialog','Yes|No','Yes','--source',702,6)
 run('linear_dialog',702,6,'--active','--past-choice')
 run('settle_arrival',698)
 run('eventq',698,69,'enter');run('settle_arrival',666)
 run('eventq',666,27,'enter');run('settle_arrival',666)
 run('eventq',666,9,'talk');run('linear_dialog',666,9,'--active')
run('eventq',666,4,'enter');run('settle_arrival',693)
run('eventq',693,4,'enter');run('settle_arrival',666)
for box,slot,incoming,outgoing in [(6,5,'Hexan','Klinklang'),(5,0,'Tranquill','Arcanine')]:
 run('eventq',666,10,'talk');run('pc_open_reviewed');run('pc_exchange_named',box,slot,incoming,outgoing)
run('party_front','Hexan','Swampert','Cofagrigus','Excadrill','Kricketune','Tranquill')
run('train_candy_one','Hexan',4,'XL')
run('give_held','Wise Glasses','Hexan')
run('teach_machine','TMX6 Dive','Swampert','Dive',3)
run('checkpoint','Amaria-roster-and-HMs-ready')
print('AMARIA PREPARATION VERIFIED; next restock and Sash coast',flush=True)
