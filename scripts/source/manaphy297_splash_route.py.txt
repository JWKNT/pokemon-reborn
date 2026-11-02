"""Follow inspected Splash Grounds doors and collect their three gems through UI."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='0.10')
def run(n,*a):
 print('SPLASH',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
def event(e,kind='enter'):run('eventq',862,e,kind)
def door(e,label):
 event(e,'talk');run('dialog','--yes','--limit',10,'--story-burst');run('checkpoint',label);event(e)
event(66);event(159,'item');event(6)
for e in [118,119,117]:event(e,'item')
door(123,'Manaphy297-Gate1')
for e in [38,48,100]:event(e)
event(155,'item');door(76,'Manaphy297-Gate2')
event(72);event(166,'item');door(70,'Manaphy297-Gate3')
event(151,'item');run('q','862,13,10');run('checkpoint','Manaphy297-Approach')
