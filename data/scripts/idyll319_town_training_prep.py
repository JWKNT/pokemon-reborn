"""Bank all four flowers and prepare Latias/fishing team through normal UI."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',879,3,'enter')
run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',2);run('pc_exchange_named',19,5,'Latias','Amoonguss','--box',2)
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',1);run('pc_exchange_named',23,2,'Arcanine','Zeraora','--box',1)
run('give_held','Safety Goggles','Magearna','--single-step')
run('field_medicine','Timid Mint','Latias');assert 'becomes timid' in read().lower();act('c','wait:.7');run('overworld')
run('give_held','Power Weight','Latias','--single-step');run('party_lead','Latias')
run('checkpoint','Idyll319-LatiasTrainingPrepared')
