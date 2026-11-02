"""Reviewed, ordinary-UI Circus speed preparation. Stops on unexpected results."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',355,136,'talk');run('mart_open')
for item,n in [('Kelpsy Berry',2),('Qualot Berry',3),('Grepa Berry',1)]:run('shop_buy',item,n,500)
run('mart_exit')
for item,n in [('Kelpsy Berry',2),('Qualot Berry',3),('Grepa Berry',1)]:run('berry_batch',item,'Hexan',n)
run('give_held','Power Anklet','Hexan');run('party_lead','Hexan')
run('checkpoint','Ciel-speed-pretraining')
s=json.loads((ROOT/'notes/Ciel-speed-pretraining-status.json').read_text())
assert next(m for m in s['party']if m['name']=='Arcanine')['ability']=='INTIMIDATE'
h=next(m for m in s['party']if m['name']=='Hexan');assert h['ev']==[252,0,75,41,0,42],h['ev']
assert s['trainer']['money']==2160,s['trainer']['money']
print('PREPARATION VERIFIED; READY FOR EIGHT POWER-ANKLET KOS',flush=True)
