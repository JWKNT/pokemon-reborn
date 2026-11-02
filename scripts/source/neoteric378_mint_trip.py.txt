"""Normal travel to the Nightclub's one-BP nature mints."""
from play import *
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',233,13,'enter');run('city_enter',233,232)
run('fly_to',527,'--carrier','Rayquaza')
run('city_enter',527,826);run('city_enter',826,827)
run('eventq',827,93,'talk')
run('bp_store_buy',15,2,'Quiet Mint')
run('bp_store_buy',1,1,'Brave Mint')
run('bp_store_buy',5,1,'Relaxed Mint')
run('bp_store_exit');run('overworld')
run('checkpoint','Neoteric378-Mints-purchased')
