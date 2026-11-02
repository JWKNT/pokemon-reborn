"""Buy capture supplies and travel to the inspected Route3 portal normally."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('DEPART',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open');run('shop_buy','Timer Ball',20,1000);run('mart_exit')
run('city_enter',369,520);run('fly_to',413,'--carrier','Zapdos');run('eventq',413,62,'enter');run('eventq',418,5,'enter')
run('q','361,53,17,right,wait:2');run('eventq',404,51,'enter');run('checkpoint','Postgame251-Route3')
run('eventq',405,15,'enter');run('play','wait:3');run('linear_dialog',835,30,'--source-page',0)
run('checkpoint','Postgame251-SwordsEntry')
