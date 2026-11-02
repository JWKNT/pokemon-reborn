"""Bounded normal UI nature/TM preparation and four reviewed Silva training fights."""
from play import *
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[]
for item,name in [('Quiet Mint','Kyogre'),('Quiet Mint','Magearna'),('Brave Mint','Rayquaza'),('Relaxed Mint','Amoonguss')]:
 steps += [('field_medicine',item,name),('overworld',)]
steps += [('teach_machine','TM92','Cresselia','Trick Room',0),('teach_machine','TM17','Magearna','Protect',0),('teach_machine','TM17','Kyogre','Protect',0),('teach_machine','TM04','Kyogre','Calm Mind',2),('checkpoint','Neoteric378-Moves-and-natures'),('city_enter',827,826),('city_enter',826,527),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('checkpoint','Neoteric378-Training-ready')]
steps += [('silva367_round',f'Postgame378-Silva{i}') for i in range(1,5)]
p=ROOT/'work/neoteric378-training-queue.json'
j=json.loads(p.read_text()) if p.exists() else {'done':0,'steps':steps}
assert j.get('pending') is None,'Prior command outcome needs manual review before queue resume'
for i in range(j['done'],len(steps)):
 step=steps[i];j['pending']={'index':i,'command':step,'epoch':time.time()};p.write_text(json.dumps(j,indent=2)+'\n')
 print('NEOTERIC PREPARATION',i,*step,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{step[0]}.py'),*map(str,step[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
print('PREPARATION AND FOUR TRAINING ROUNDS COMPLETE',flush=True)
