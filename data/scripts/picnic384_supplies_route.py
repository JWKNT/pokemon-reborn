"""Return after both saved captures using normal menus; accept the desert follow-up."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('party_front', 'Magearna', 'Kyogre'), ('city_enter', 827, 826), ('city_enter', 826, 527), ('fly_to', 519, '--carrier', 'Rayquaza'), ('city_enter', 519, 38), ('eventq', 38, 5, 'talk'), ('mart_open',), ('shop_buy', 'Ultra Potion', 12, 1200), ('shop_buy', 'Revive', 5, 1500), ('shop_buy', 'Super Repel', 5, 700), ('mart_exit',), ('checkpoint', 'Picnic384-Supplies'), ('city_enter', 38, 519), ('fly_to', 525, '--carrier', 'Rayquaza'), ('connected_walk', 525, 551, 15, 12), ('connected_walk', 551, 552, 20, 8), ('connected_walk', 552, 544), ('eventq', 544, 12, 'enter'), ('eventq', 150, 313, 'talk'), ('choose_dialog', 'Yes|No', 'Yes'), ('overworld',), ('checkpoint', 'Picnic384-Summit')]
p=R/'work/picnic384-supplies-route.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('PICNIC SUPPLIES384',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
