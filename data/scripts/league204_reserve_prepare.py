"""Normal Circus reserve leveling and route preparation, with saved-state guards."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('PREP',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
s=json.loads((R/'notes/Prep204-Indra-8-status.json').read_text())
assert s['map']==355 and s['bag']['contents']['EXPCANDYXL']>=10
assert s['party'][3]['name']=='Mienshao' and s['party'][4]['name']=='Hexan'
for slot,party,name,out in [(5,3,'Cofagrigus','Mienshao'),(15,4,'Excadrill','Hexan')]:
 if not ('--at-pc' in sys.argv and slot==5):run('eventq',355,5,'talk')
 run('pc_open_reviewed');run('pc_exchange_named',slot,party,name,out)
run('checkpoint','Prep204-Reserves')
run('league203_candy_spend','Prep204-Reserves','Cofagrigus','Excadrill')
run('eventq',355,5,'talk');run('pc_open_reviewed');run('pc_exchange_named',5,3,'Mienshao','Cofagrigus')
run('teach_machine','TMX4','Mienshao','Strength',3)
run('eventq',355,90,'talk');run('mart_open');run('shop_buy','Super Repel',12,700);run('mart_exit')
run('checkpoint','Prep204-Travel-ready')
run('field_repel','Super Repel')
run('league202_scales','scrapyard')
