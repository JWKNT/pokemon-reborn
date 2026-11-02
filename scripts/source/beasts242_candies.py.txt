"""Apply planned, count-verified candies via normal menus; stop on uncertainty."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,env=env)
for name,count in [('Cresselia',14),('Zapdos',14),('Swampert',12),('Hexan',9),('Cofagrigus',8),('Mawile',4)]:
 run('train_candy_one',name,count,'XL')
run('eventq',38,3,'talk')
run('heal')
run('checkpoint','Postgame242-BeastsTeam')
