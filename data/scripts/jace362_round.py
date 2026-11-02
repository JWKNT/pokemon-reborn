"""Reviewed Jace v4 funding round with bulky Arcanine and Amulet Coin."""
import json,os,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
label=sys.argv[1]
assert re.fullmatch(r'Postgame362-Jace[1-3]',label)
assert not (ROOT/'notes'/f'{label}-status.json').exists()
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(name,*args):
    print('JACE FUNDING',name,*args,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)],check=True)
foes=['Drifblim','Watchog','Cherrim','Comfey','Bisharp']
(ROOT/'notes/battle-control.json').write_text(json.dumps({'expected_foes':foes,'scope':'Installed Jace v4 level83–86; Arcanine140 Flamethrower1, full529HP before each round.'}))
run('party_front','Arcanine')
run('overworld')
run('eventq',38,42,'talk')
run('trainer_music','start','COOLTRAINER_Male','Jace','--map',38)
run('choose_dialog','Yes|No','Yes')
run('trainer_enter',38,42,'COOLTRAINER_Male','Jace','--expand-common','--active-dialogue','--past-choice','--resume-intro')
run('battle_batch','Arcanine',1,'--foes',','.join(foes),'--turns',10,'--stay','--stay-team-reviewed','--watch','--min-hp',.40,'--recover-below',.65,'--recover-slot',3,'--stop-after-victory')
run('grandhall_reward')
run('overworld')
run('trainer_music','finish','--world-verified')
run('checkpoint',label)
v=json.loads((ROOT/'notes'/f'{label}-status.json').read_text())
assert v['map']==38 and all(p['hp']==p['totalhp'] and p['status'] is None for p in v['party'])
print('ROUND VERIFIED',v['trainer']['money'],v['bag']['contents']['EXPCANDYXL'],flush=True)
