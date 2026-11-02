"""Reviewed native menus and Fly travel for Adrienn preparation; stop on failure."""
from play import ROOT
import subprocess,sys,json

def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
s=json.loads((ROOT/'notes/Devon-city-healed-status.json').read_text())
assert s['map']==83 and all(p['hp']==p['totalhp'] for p in s['party'])
assert s['party'][4]['species']=='AMPHAROS'
run('eventq.py',83,7,'talk')
run('pc_open_reviewed.py')
run('pc_exchange_named.py',11,4,'Tranquill','Ampharos')
run('eventq.py',83,8,'enter')
run('fly_to.py',355)
run('eventq.py',355,83,'talk')
run('mart_open.py')
run('shop_buy.py','Power Bracer',1,15000)
run('shop_buy.py','Power Weight',1,15000)
run('mart_exit.py')
print('CIRCUS POWER ITEMS BOUGHT',flush=True)
