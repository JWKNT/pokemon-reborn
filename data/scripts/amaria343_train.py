"""Take the reviewed Tourmaline train using the ticket kiosk."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TRAIN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',591,6,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',591,6,'--active','--past-choice');run('checkpoint','Amaria343-Ticket');run('eventq',591,19,'enter')
