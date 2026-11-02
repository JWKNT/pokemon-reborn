"""Normal UI travel to the inspected Diancie lead and Aegir entrance."""
import os,subprocess,sys,pathlib,json
R=pathlib.Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('DIANCIE ROUTE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('city_enter',38,519);run('fly_to',527,'--carrier','Altaria')
run('city_enter',527,826);run('city_enter',826,827)
run('eventq',827,82,'talk')
run('linear_dialog',827,82,'--source-page',6,'--until-choice','--burst')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',827,82,'--source-page',6,'--after-last-choice','--past-choice','--burst')
run('checkpoint','Diancie268-Quest')
s=json.loads((R/'notes/Diancie268-Quest-navigation.json').read_text());assert s['variables']['626']==1
run('city_enter',827,826);run('city_enter',826,527)
run('fly_to',781,'--carrier','Altaria')
run('city_enter',781,783);run('city_enter',783,812);run('city_enter',812,785)
run('city_enter',785,852);run('city_enter',852,849)
run('checkpoint','Diancie268-Aegir')
