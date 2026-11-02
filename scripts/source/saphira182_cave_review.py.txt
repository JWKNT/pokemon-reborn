"""Offline explicit damage estimates using installed rosters and frozen owned save."""
import json,math
from pathlib import Path
from saphira_damage_review import stats,NATURES
from glass_damage_review import damage
R=Path(__file__).resolve().parents[1]
NATURES.update(BRAVE=(1,5),RELAXED=(2,5))
sp=json.loads((R/'work/saphira-capture-options-source.json').read_text())['species']
sp['GYARADOS']={'Normal Form':{'BaseStats':[95,125,79,60,100,81]}} # installed montext.rb:9259
foes={m['species']:stats(m,sp,'Mega X Form' if m['species']=='CHARIZARD' else None) for m in json.loads((R/'work/saphira-installed-team.json').read_text())[0][1]}
us={m['species']:m for m in json.loads((R/'notes/Gyarados181-Indra-6-status.json').read_text())['party']}
sw=us['SWAMPERT'];gy=dict(us['GYARADOS'],level=95,ev=[0,252,0,0,0,252]);gs=stats(gy,sp)
n=foes['NOIVERN'];out=[]
for field,f in [('Dragon Den',1.5),('Cave',1)]:
 for stage,mult in [(0,1),(2,2),(4,3)]:
  for actor,d,h in [('Swampert',sw['spdef'],sw['totalhp']),('Gyarados',gs[4],gs[0])]:
   out.append({'label':f'{field} Seed Noivern Dragon Pulse vs {actor} SpDef+{stage}','range':damage(95,85,n[3]*1.5,d*mult,base_modifier=f,modifier=1.5),'hp':h})
for field,f,df in [('Dragon Den',1.5,1.3),('Cave',1,1)]:
 for name,st in foes.items():
  mod=1 if field=='Dragon Den' and name=='DRAGONITE' else 2
  multiscale=.5 if name=='DRAGONITE' else 1
  out.append({'label':f'{field} +4 Gyarados Outrage vs full {name}','range':damage(95,120,gs[1]*3,st[2]*df,base_modifier=f,modifier=mod*multiscale),'hp':st[0],'note':'Sash and Rough Skin remain relevant; no STAB for Gyarados.'})
print(json.dumps({'scope':'Offline explicit planning estimates, intermediate rounding uncertainty; no runtime state or AI.','foes':foes,'planned_gyarados':gs,'reports':out},indent=2))
