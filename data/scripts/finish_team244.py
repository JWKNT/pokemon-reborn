"""Return from paired training and assemble the reviewed Suicune team via UI."""
import os, subprocess, sys, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(script,*args):
 print('FINAL TEAM244',script,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{script}.py'),*map(str,args)],env=env,check=True)
phase=sys.argv[1]
if phase=='return':
 run('field_repel','Super Repel')
 run('city_enter',633,519)
 run('fly_to',519,'--carrier','Zapdos')
 run('city_enter',519,38)
 run('q','38,5,22,up:.12')
 run('heal')
 run('q','38,9,20,up:.12,c,wait:1')
 run('pc_open_reviewed')
elif phase=='take':run('pc_take_item244')
elif phase=='swap':
 run('q','38,9,20,up:.12,c,wait:1')
 run('pc_open_reviewed')
 run('pc_exchange_named',24,1,'Cresselia','Swampert')
elif phase=='items':
 run('give_held','Spell Tag','Aegislash','--single-step')
 run('give_held','Wide Lens','Walrein','--single-step')
 run('checkpoint','Postgame244-SuicuneTeamReady')
 s=json.loads((R/'notes/Postgame244-SuicuneTeamReady-status.json').read_text())
 assert s['map']==38
 assert {m['species'] for m in s['party']}=={'WALREIN','CRESSELIA','ZAPDOS','CRYOGONAL','MAWILE','AEGISLASH'}
 assert all(m['hp']==m['totalhp'] and m['status'] is None and m['level']==110 for m in s['party'])
 print('SUICUNE TEAM READY',flush=True)
else:raise SystemExit('Unknown phase')
