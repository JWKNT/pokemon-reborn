"""One Saturday Carol v4 training round, using a reviewed capped Mawile."""
import json, os, re, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_CHUNK='84')
label=sys.argv[1];assert re.fullmatch(r'Postgame\d+-Carol\d+',label)
assert not (R/'notes'/f'{label}-status.json').exists()
def run(s,*a):
 print('CAROL ROUND',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
p=R/'notes/battle-control.json';d=json.loads(p.read_text());d.update(stop=False,expected_foes=['Meowstic','Feraligatr','Furret','Furfrou','Meganium']);p.write_text(json.dumps(d,indent=2)+'\n')
run('party_lead','Mawile')
run('eventq',38,52,'talk')
run('trainer_music','start','COOLTRAINER_Female','Carol','--map',38)
run('choose_dialog','Yes|No','Yes')
run('trainer_enter',38,52,'COOLTRAINER_Female','Carol','--expand-common','--active-dialogue','--past-choice','--resume-intro')
run('battle_move',3,'--mega','--watch')
run('battle_batch','Mawile',0,'--foes','meowstic,feraligatr,furret,furfrou,meganium','--foe-slots',json.dumps({'meowstic':0,'feraligatr':0,'furret':0,'furfrou':0,'meganium':1}),'--turns',14,'--stay','--min-hp',.30,'--watch','--stop-after-victory')
# Public victory is mandatory; this refuses to proceed if the HP/matchup guard stopped.
run('grandhall_reward');run('overworld');run('trainer_music','finish','--world-verified');run('checkpoint',label)
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert s['map']==38 and all(m['hp']==m['totalhp'] and m['status'] is None for m in s['party'])
print('CAROL ROUND VERIFIED',label,'XL',s['bag']['contents'].get('EXPCANDYXL'),flush=True)
