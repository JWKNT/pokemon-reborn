"""Restock the planned Ciel item budget through ordinary, price-verified mart UI."""
from play import *
from locate import locate
assert locate(355)[0] == 355
s=json.loads((ROOT/'notes/Ciel-circus-arrival-status.json').read_text())
assert s['map']==355 and s['trainer']['badges'].count(True)==12
stock=s['bag']['contents']
plan=[('HYPERPOTION','Hyper Potion',16,1000),('FULLHEAL','Full Heal',8,600),('COTTONCANDY','Cotton Candy',6,5000)]
need=[(label,max(0,n-stock.get(code,0)),price)for code,label,n,price in plan]
assert s['trainer']['money']>=sum(n*price for label,n,price in need)+2000,'Supply budget needs review'
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
run('eventq',355,90,'talk');run('mart_open')
for label,n,price in need[:2]:
 if n:run('shop_buy',label,n,price)
run('mart_exit');run('eventq',355,29,'talk');run('mart_open')
label,n,price=need[2]
if n:run('shop_buy',label,n,price)
run('mart_exit');run('party_lead','Ampharos')
print('CIEL RESTOCK VERIFIED',need,flush=True)
