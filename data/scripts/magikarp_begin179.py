"""Start the normal Magikarp quest; halt after the first inspected double battle."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q','battle_move']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
if '--quest-started' not in sys.argv:
 run('party_front','Swampert','Gigalith','Arcanine','Sylveon','Cofagrigus','Tranquill')
 run('eventq',519,116,'enter');run('eventq',38,34,'talk')
 run('choose_dialog','Yes|No','Yes','--source',38,34)
 run('linear_dialog',38,34,'--active','--past-choice')
 run('checkpoint','Magikarp179-started')
s=json.loads((R/'notes/Magikarp179-started-navigation.json').read_text());assert s['variables']['155']==1
if '--opal-outside' not in sys.argv:run('eventq',38,6,'enter')
run('fly_to',530,'--carrier','Tranquill');run('eventq',530,11,'enter')
run('eventq',522,27,'enter');run('checkpoint','Magikarp179-goons-ready')
run('eventq',62,5,'talk');run('choose_dialog','Yes|No','Yes','--source',62,5)
run('trainer_enter',62,5,'StreetRat','Arnie & Milhouse','--active-dialogue','--past-choice')
run('battle_ready')
from play import read,act
p=R/'notes/current-run-control.json';c=json.loads(p.read_text())
t=read().lower();assert 'fight' in t and 'bag' in t
assert not c.get('battle_turbo_enabled') and not c.get('overworld_turbo_enabled')
act('m:.12','wait:.5');c.update(battle_turbo_enabled=True,battle_turbo=True);p.write_text(json.dumps(c,indent=2))
# Both Lv11 foes are vulnerable to the reviewed spread Rock Slide;
# the two level95 leads have it in slot3. Guard each public actor prompt.
t=read().lower();assert 'swampert' in t or 'suampert' in t
run('battle_move',3,'--watch')
run('battle_ready');t=read().lower();assert 'gigalith' in t
run('battle_move',3,'--watch');run('battle_ready')
print('FIRST QUEST DOUBLE BATTLE REVIEW',flush=True)
