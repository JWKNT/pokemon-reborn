"""Bring the saved Complete Zygarde to Shelly through normal travel."""
import os,subprocess,sys
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.12')
steps=[('city_enter',827,826),('city_enter',826,527),('fly_to',525,'--carrier','Rayquaza'),('connected_walk',525,544,8,7),('eventq',544,12,'enter'),('city_enter',150,153),('eventq',153,133,'talk')]
for s,*a in steps:
 print('PICNIC384',s,*a,flush=True)
 subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
