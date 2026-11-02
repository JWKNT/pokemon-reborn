"""Reviewed post-sticker supplies and roster exchanges through ordinary UI."""
from play import *
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
r('city_enter',4,113)
r('eventq',113,1,'talk');act('c','wait:.6','c','wait:.6')
r('dept_floor',1);r('city_enter',112,520);r('city_enter',520,611)
r('eventq',611,2,'talk');r('mart_open');r('shop_buy','Revival Herb',3,2800);r('mart_exit')
r('city_enter',611,520);r('fly_to',519);r('city_enter',519,38)
r('eventq',38,5,'talk');r('mart_open');r('shop_buy','Ultra Potion',5,1200);r('mart_exit')
r('eventq',38,3,'talk');r('heal')
for b,p,incoming,outgoing in [(1,0,'Swampert','Ampharos'),(5,5,'Kricketune','Tranquill')]:
 r('eventq',38,4,'talk');r('pc_open_reviewed');r('pc_exchange_named',b,p,incoming,outgoing)
r('party_front','Excadrill','Swampert','Arcanine','Cofagrigus','Klinklang','Kricketune')
r('checkpoint','Castle-prep-complete')
s=json.loads((ROOT/'notes/Castle-prep-complete-status.json').read_text())
assert [m['name']for m in s['party']]==['Excadrill','Swampert','Arcanine','Cofagrigus','Klinklang','Kricketune']
assert all(m['hp']==m['totalhp']for m in s['party'])
print('CASTLE PREPARATION VERIFIED',s['trainer']['money'],flush=True)
