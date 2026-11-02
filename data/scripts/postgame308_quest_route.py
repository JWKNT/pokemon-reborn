"""Normal NPC quest acceptance and recorded travel to the Tanzan crystal room."""
import os,sys,subprocess
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('MEWTWO APPROACH',n,*a,flush=True);subprocess.run([sys.executable,'scripts/'+n+'.py',*map(str,a)],check=True)
run('party_front','Mawile','Cresselia','Magearna','Zapdos','Volcanion','Swampert')
run('city_enter',38,519);run('fly_to',527,'--carrier','Zapdos');run('city_enter',527,826);run('city_enter',826,827)
run('eventq',827,81,'talk');run('linear_dialog',827,81,'--source-page',6,'--until-choice');run('choose_dialog','Yes|No','Yes');run('linear_dialog',827,81,'--source-page',6,'--past-choice','--after-last-choice')
run('checkpoint','Mewtwo308-Quest')
run('city_enter',827,826);run('city_enter',826,527);run('fly_to',232,'--carrier','Zapdos');run('field_repel','Super Repel');run('surface_walk',232,18,67);run('eventq',232,1,'enter');run('city_enter',231,272);run('city_enter',272,273);run('checkpoint','Mewtwo308-CrystalRoom')
