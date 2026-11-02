"""Reviewed installed hole/ladder sequence, ordinary Strength pushes and saved checks."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LADDERS',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
def enter(e):run('eventq',279,e,'enter')
def push(e,d,n,label):
 run('wall309_strength');run('wasteland309_push',279,e,d,n,'Wasteland309-'+label)
run('city_enter',277,278);run('eventq',278,2,'enter')
enter(19)
push(1,'right',4,'Drop1')
enter(21)
push(31,'right',4,'BottomClear1')
enter(10);enter(13)
push(3,'left',3,'Drop2')
enter(20);enter(22);enter(28)
enter(19);enter(21);enter(10)
push(26,'right',15,'Drop3')
enter(22)
push(29,'right',3,'BottomClear3')
enter(14);enter(16);enter(4)
run('checkpoint','Wasteland309-BeforeFern')
print('STOPPED BEFORE FERN ROOM',flush=True)
