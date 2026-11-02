"""Buy reviewed Fiore/Ciel supplies at the circus, through verified shop UI."""
from play import *
from locate import locate
assert locate(355)[0]==355
cash=json.loads((ROOT/'notes/WTC-Ace-won-status.json').read_text())['trainer']['money']
# Reborn 19.5 Super Repels cost 700, and last 400 steps.
hyper,repels,cotton=12,8,4
if cash<hyper*1000+repels*700+cotton*5000:
 hyper,repels,cotton=10,6,3
assert cash>=hyper*1000+repels*700+cotton*5000,'Supply budget needs review'
def run(n,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(n+'.py')),*map(str,args)],check=True)
run('eventq',355,90,'talk');run('mart_open')
run('shop_buy','Hyper Potion',hyper,1000)
run('shop_buy','Super Repel',repels,700)
run('mart_exit')
run('eventq',355,29,'talk');run('mart_open')
run('shop_buy','Cotton Candy',cotton,5000)
run('mart_exit')
run('party_lead','Cofagrigus')
print('FIORE SUPPLIES / FIXED COFAGRIGUS LEAD READY',hyper,repels,cotton,flush=True)
