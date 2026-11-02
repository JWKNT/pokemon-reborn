"""Normal fixed-budget Aegir shopping from a verified Grand Hall checkpoint."""
from play import *
def run(s,*a):
 print('AEGIR RESTOCK',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((ROOT/'notes/Aegir369-ReminderComplete-status.json').read_text())
assert s['map']==38 and s['bag']['contents'].get('POWERANKLET',0)>=2
assert s['trainer']['money']+7500>=22900
run('eventq',38,5,'talk');run('choose_dialog','Buy|Sell|Quit','Sell')
run('shop_sell_one','Power Anklet',7500);run('mart_exit')
run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Ultra Potion',8,1200);run('shop_buy','Super Repel',5,700);run('mart_exit')
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open')
run('shop_buy','Heavy Ball',30,300);run('mart_exit')
run('city_enter',369,520);run('eventq',520,101,'enter');run('eventq',112,6,'enter')
run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',2)
run('eventq',114,2,'talk');run('mart_open');run('shop_buy','Chesto Berry',2,400);run('mart_exit')
run('give_held','Chesto Berry','Heatran','--pocket','Berries')
run('give_held','Chesto Berry','Cresselia','--pocket','Berries')
run('eventq',114,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1)
run('eventq',112,1,'enter');run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
run('eventq',38,3,'talk');run('heal');run('checkpoint','Aegir369-Supplies')
