"""Assemble owned supports and take the reviewed Amulet Coin for training."""
from play import *
def run(s,*args):
 print('AEGIR PREP',s,*args,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',1)
run('pc_exchange_named',23,2,'Heatran','Volcanion','--box',1,'--stay-open')
run('pc_exchange_named',16,5,'Cresselia','Zeraora','--box',1,'--stay-open')
run('pc_select_box',2)
act('right:.12','wait:.2',*['down:.12','wait:.2']*4,'c','wait:.6')
run('pc_take_owned_item',25,'Arcanine','Amulet Coin','--menu-open')
run('give_held','Amulet Coin','Zapdos')
run('party_front','Zapdos');run('checkpoint','Aegir369-TrainingParty')
for i in range(1,4):run('silva367_round','Postgame369-Silva'+str(i))
