"""Finite normal-menu preparation after one verified stolen Heart Scale."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(n,*a):
 print('NECROZMA PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('fly_to',521,'--carrier','Zapdos')
run('city_enter',521,116)
run('onyx_relearn_one','Latias','Stored Power',7,1)
run('teach_machine','TM94','Arcanine','Rock Smash',0)
run('give_held','Amulet Coin','Arcanine')
run('party_lead','Latias')
run('city_enter',116,521)
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,38)
run('eventq',38,3,'talk')
run('heal')
run('checkpoint','Necrozma365-StoredPowerPrepared')
