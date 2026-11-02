"""Normal held items, machines, PC exchange and supplies for the Neoteric boss."""
import json,os,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
s=json.loads((R/'notes/Neoteric378-KyogreCandyReady-Cap145-status.json').read_text())
assert s['map']==38 and [p['species']for p in s['party']]==['KYOGRE','RAYQUAZA','AMOONGUSS','CRESSELIA','MAGEARNA','ZAPDOS']
assert s['trainer']['money']>=44750
steps=[('give_held','Blue Orb','Kyogre','--pocket','Crystals'),('give_held','Power Weight','Magearna'),('give_held','Amplifield Rock','Cresselia'),('give_held','Safety Goggles','Amoonguss'),('teach_machine','TM92','Magearna','Trick Room',3),('teach_machine','TM16','Cresselia','Light Screen',1),('teach_machine','TM17','Rayquaza','Protect',3),('eventq',38,4,'talk'),('pc_open_reviewed',),('pc_select_box',2),('pc_exchange_named',20,5,'Heatran','Zapdos','--box',2),('eventq',38,5,'talk'),('choose_dialog','Buy|Sell|Quit','Buy'),('shop_buy','Ultra Potion',6,1200),('shop_buy','Super Repel',10,700),('shop_buy','Escape Rope',1,550),('mart_exit',),('party_front','Cresselia','Magearna'),('overworld',),('eventq',38,3,'talk'),('heal',),('checkpoint','Neoteric378-BossTeam'),('eventq',38,6,'enter'),('fly_to',520,'--carrier','Rayquaza'),('eventq',520,67,'enter'),('eventq',369,1,'talk'),('mart_open',),('shop_buy','Timer Ball',30,1000),('mart_exit',),('city_enter',369,520),('checkpoint','Neoteric378-Supplied')]
p=R/'work/neoteric378-boss-build.json';j=json.loads(p.read_text()) if p.exists() else dict(done=0,steps=steps)
assert j.get('pending') is None,'Prior outcome needs review'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('BOSS PREPARATION',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
print('BOSS TEAM AND SUPPLIES COMPLETE',flush=True)
