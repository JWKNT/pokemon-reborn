"""Reviewed level-up, Strength, and return route; stops before spring boulders."""
import subprocess,sys,os
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SPRINGS PREP',s,*a,flush=True)
 subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True,env=E)
run('postgame_candy_spend','Postgame261-Will1',120)
run('teach_machine','TMX4','Swampert','Strength',0,'--single-step')
run('give_held','Elemental Seed','Sylveon','--single-step')
run('party_front','Sylveon','Zapdos')
run('city_enter',38,519)
run('fly_to',271,'--carrier','Zapdos')
run('eventq',271,12,'enter')
run('eventq',234,256,'enter')
run('surface_walk',238,33,39)
run('checkpoint','Postgame261-SpringsBoulderApproach')
