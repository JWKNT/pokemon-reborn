"""One reviewed Rhodochrine apparition through ordinary UI; stop on changed matchup."""
import json,os,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
event=int(sys.argv[1]);actor=sys.argv[2];slot=int(sys.argv[3]);assert actor in ['Magearna','Zapdos','Volcanion','Mawile','Darkrai'] and 0<=slot<4
rows=json.loads((R/'work/331-picnic-puzzle-mons.json').read_text());row=next(m for m in rows if m['event']==event)
assert row['level']==100
source=json.loads((R/'work/331-map886-events.json').read_text())[str(event)]['pages'][0]['list']
assert not any(c['code']in[102,103,104,201,301] for c in source)
assert sum('pbWildBattle' in str(c['parameters']) for c in source)==1
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('APPARITION',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=E,check=True)
(R/'notes/battle-control.json').write_text(json.dumps({'expected_foes':[row['species']],'scope':'Installed Rhodochrine puzzle apparition'}))
lead=sys.argv[sys.argv.index('--lead')+1] if '--lead' in sys.argv else actor
assert lead==actor or (lead=='Darkrai' and actor in ['Magearna','Zapdos'])
before=json.loads((R/'notes/navigation-state.json').read_text())['variables']
start=time.time()
if '--battle-open' not in sys.argv:
 if '--same-lead' not in sys.argv:run('party_front',lead)
 run('eventq',886,event,'talk')
 run('picnic_intercept',row['species'],*(['--dark'] if row['ops'][0][0]==662 else []))
run('battle_ready')
if lead!=actor:
 import re,unicodedata
 text=subprocess.check_output([sys.executable,str(R/'scripts/play.py')],env=E,text=True)
 norm=lambda x:re.sub('[^a-z]','',unicodedata.normalize('NFKD',x.lower()))
 assert norm(row['species']) in norm(text) and norm(lead) in norm(text), 'Public lead/foe review before switch'
 run('battle_switch',actor)
 run('battle_ready')
run('battle_batch',actor,slot,'--foes',row['species'],'--wild','--turns',5,'--min-hp',.45,'--watch')
run('overworld')
label=f'Picnic332-Apparition{event}'
run('checkpoint',label)
after=json.loads((R/'notes'/f'{label}-navigation.json').read_text())['variables']
for op in row['ops']:
 assert after[str(op[0])]==before[str(op[0])]-op[4], 'Expected puzzle power was not removed; review moving apparition interaction'
run('close_wild_music',row['species'],'--since',start)
print('APPARITION WORLD RETURNED',event,row['species'],flush=True)
